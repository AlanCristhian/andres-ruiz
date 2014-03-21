"""
Provides a class to handle an sqlite3 database system.
"""

import atexit
import collections
import re
import sqlite3
import datetime
import time


from framework.helpers import JavaScriptObject
from framework.helpers import Flyeight


class Connection(sqlite3.Connection, metaclass=Flyeight):
    """All instances of the sqlite3.Connection class that have the same
    database file are the same instance. But each cursor is an different
    object. This will solve the problems of locks when do columns changes
    mixed with rows changes.
    """
    pass


class Collection:
    """An abstraction layer to admin tables from sqlite3 databases.
    This class not manage the contents of the tables.
    """
    def __init__(self, dbpath):
        self.dbpath = dbpath
        # !!!: Remember that you must update the self._format_parameters method
        # if you update the self type property.
        self.type = {
            'int': 'INTEGER'
            ,'float': 'REAL'
            ,'str': 'TEXT'
            ,'bytes': 'BLOB'
            ,'prim': 'PRIMARY KEY'
            ,'intPrim': 'INTEGER PRIMARY KEY'
            ,'bool': 'BOOLEAN'
            ,'date': 'DATE'
            ,'datetime': 'TIMESTAMP'
        }
        self.validTypes = set(self.type.keys())
        self.bindingDict = {}

        # Adapters and converters for the bool type
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
        self.connection = Connection(
            self.dbpath
            ,check_same_thread=False
            ,detect_types=sqlite3.PARSE_DECLTYPES)
        atexit.register(self._finalize)

    def path(self, dbpath=None):
        """Get an str and set dbpath as new database file and return the self
        instance. If not argument return a str with the path of database file.
        """
        if dbpath:
            self.dbpath = dbpath
            return self
        else:
            return self.dbpath

    def get(self, tableName):
        """Return an instance of the sqlite3Model class.
        Keyword arguments:
            tableName -- the name of the table binding to sqlite3Model class.
        """
        return Model(tableName, self.connection)

    def has(self, tableName): # 2 consult
        """Return True if the table name exists into the database.
        Else return False.
        Keyword arguments:
            name -- the table-name to check.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sqlite_master WHERE type=? AND name=?", ('table', tableName))
        tableCount = cursor.fetchall()
        cursor.close()
        return True if len(tableCount) else False

    def save(self):
        """save changes into database."""
        self.connection.commit()
        return self

    def remove_fields(self, name, fields):
        """remove columns of the table"""
        keys = self._fields(name)
        if isinstance(fields, str):
            keys.remove(fields)

        elif isinstance(fields, tuple) or isinstance(fields, list):
            for field in fields:
                keys.remove(field)
        else:
            raise TypeError('The "fields" parameter must be str, tuple or list type.')
        columns = ', '.join(keys)
        self._result = \
"""BEGIN TRANSACTION;
CREATE TEMPORARY TABLE table_backup({fields});
INSERT INTO table_backup SELECT {fields} FROM {name};
DROP TABLE {name};
CREATE TABLE {name}({fields});
INSERT INTO {name} SELECT {fields} FROM table_backup;
DROP TABLE table_backup;
COMMIT;
VACUUM;""".format(name=name, fields=columns)
        self.connection.executescript(self._result)
        return self

    def _fields(self, name):
        """return the info of table."""
        query = 'SELECT * FROM {name}'.format(name=name)
        cursor = self.connection.execute(query)
        return list(map(lambda x: x[0], cursor.description))

    def add_fields(self, name, fields):
        """add columns into an existing table"""
        fieldsTypes = set(fields.values())
        if not fieldsTypes.issubset(self.validTypes):
            self.validTypes = self.validTypes.difference(fieldsTypes)
            raise KeyError('"' + self.validTypes + '" is an invalid type of field.')
        query = 'ALTER TABLE {name} ADD COLUMN {fields}'
        # values sorted by key
        sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
        rows = (
            query.format(name=name, fields=key + ' ' + self.type[sortedFields[key]]) \
            for key in sortedFields.keys()
        )
        result = ';\n'.join(rows)
        if len(fields) == 1:
            self.connection.execute(result)
        else:
            self.connection.executescript(result)
        return self

    def _finalize(self):
        """commit the changes and close the database."""
        if self.connection.in_transaction:
            self.connection.commit()
        self.connection.close()

    def create(self, name, fields):
        """Create a table into the database and return the self instance.
        Keyword arguments:
            name -- the name of the new model.
            fields -- an dictionary with fields has key and types has values.
        """
        fieldsTypes = set(fields.values())
        if not fieldsTypes.issubset(self.validTypes):
            self.validTypes = self.validTypes.difference(fieldsTypes)
            raise KeyError('"%s" is an invalid type of field.' % self.validTypes)
        # template to create an table
        query = 'CREATE TABLE IF NOT EXISTS {name} ({fields})'
        # values sorted by key
        sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
        rows = (key + ' ' + self.type[sortedFields[key]] for key in sortedFields.keys())
        fields = ', '.join(rows)
        # fill the template
        result = query.format(
            name=name,
            fields=fields)
        self.connection.execute(result)
        return self

    def remove(self, name):
        """Remove the table of the database and return the self instance.
        Keyword arguments:
            name -- the name of table to clear.
        """
        result = 'DROP TABLE IF EXISTS {name}'.format(name=name)
        self.connection.execute(result)
        return self

    def bind(self, bindName, modelSource, fieldSource, modelTarget, fieldTarget):
        """Link the model source with modelTarget in a n-1 relationship and
        return the self instance.
        Keyword arguments:
            bindName -- the name of the bind.
            modelSource -- the table name to be linked
            fieldSource -- the field of the table to be linked
            modelTarget -- the table name that condition modelSource consultations
            fieldTarget -- the field of the table that condition modelSource consultations
        """
        self.bindingDict[bindName] = {
            'bindName': bindName
            ,'modelSource': modelSource
            ,'fieldSource': fieldSource
            ,'modelTarget': modelTarget
            ,'fieldTarget': fieldTarget
        }
        template = \
"""CREATE TRIGGER IF NOT EXISTS update_{fieldSource}_on_{modelSource}_when_update_{fieldTarget}_in_{modelTarget}_{bindName}
    AFTER UPDATE ON {modelTarget}
        FOR EACH ROW BEGIN
            UPDATE {modelSource} SET {fieldSource} = NEW.{fieldTarget} WHERE {modelSource}.{fieldSource} = OLD.{fieldTarget};
        END;

CREATE TRIGGER IF NOT EXISTS delete_{modelSource}_when_delete_{fieldTarget}_from_{modelTarget}_{bindName}
    BEFORE DELETE ON {modelTarget}
        FOR EACH ROW BEGIN
            DELETE FROM {modelSource} WHERE {modelSource}.{fieldSource} = OLD.{fieldTarget};
        END;

CREATE TRIGGER IF NOT EXISTS do_not_insert_{modelSource}_with_invalid_{fieldSource}_{bindName}
    BEFORE INSERT ON {modelSource}
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't insert the register")
            WHERE (SELECT {fieldTarget} FROM {modelTarget} WHERE {modelTarget}.{fieldTarget}=NEW.{fieldSource}) IS NULL;
        END;

CREATE TRIGGER IF NOT EXISTS do_not_update_{fieldSource}_on_{modelSource}_with_invalid_{fieldSource}_{bindName}
    BEFORE UPDATE ON {modelSource} 
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't update the register")
            WHERE (SELECT {fieldTarget} FROM {modelTarget} WHERE {modelTarget}.{fieldTarget}=NEW.{fieldSource}) IS NULL;
        END;"""

        # The clause "IF NOT EXISTS" can trow an sintax error
        template2 = \
"""CREATE TRIGGER update_{fieldSource}_on_{modelSource}_when_update_{fieldTarget}_in_{modelTarget}_{bindName}
    AFTER UPDATE ON {modelTarget}
        FOR EACH ROW BEGIN
            UPDATE {modelSource} SET {fieldSource} = NEW.{fieldTarget} WHERE {modelSource}.{fieldSource} = OLD.{fieldTarget};
        END;

CREATE TRIGGER delete_{modelSource}_when_delete_{fieldTarget}_from_{modelTarget}_{bindName}
    BEFORE DELETE ON {modelTarget}
        FOR EACH ROW BEGIN
            DELETE FROM {modelSource} WHERE {modelSource}.{fieldSource} = OLD.{fieldTarget};
        END;

CREATE TRIGGER do_not_insert_{modelSource}_with_invalid_{fieldSource}_{bindName}
    BEFORE INSERT ON {modelSource}
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't insert the register")
            WHERE (SELECT {fieldTarget} FROM {modelTarget} WHERE {modelTarget}.{fieldTarget}=NEW.{fieldSource}) IS NULL;
        END;

CREATE TRIGGER do_not_update_{fieldSource}_on_{modelSource}_with_invalid_{fieldSource}_{bindName}
    BEFORE UPDATE ON {modelSource} 
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't update the register")
            WHERE (SELECT {fieldTarget} FROM {modelTarget} WHERE {modelTarget}.{fieldTarget}=NEW.{fieldSource}) IS NULL;
        END;"""

        result = template.format(
            bindName=bindName
            ,modelSource=modelSource
            ,fieldSource=fieldSource
            ,modelTarget=modelTarget
            ,fieldTarget=fieldTarget)

        result2 = template2.format(
            bindName=bindName
            ,modelSource=modelSource
            ,fieldSource=fieldSource
            ,modelTarget=modelTarget
            ,fieldTarget=fieldTarget)

        try:
            self.connection.executescript(result)
        except sqlite3.OperationalError as e:
            if e.args[0] == 'near "NOT": syntax error':
                self.connection.executescript(result2)
            else:
                raise e

        return self

    # BUG: the gindingDict isn't store anyway
    def unbind(self, bindName):
        """remove the triggers creates for bind.
        Keyword arguments:
            bindName -- the name of bind to remove
        """
        bind = self.bindingDict.get(bindName)
        if bind:
            template = \
"""DROP TRIGGER IF EXISTS update_{fieldSource}_on_{modelSource}_when_update_{fieldTarget}_in_{modelTarget}_{bindName};
DROP TRIGGER IF EXISTS delete_{modelSource}_when_delete_{fieldTarget}_from_{modelTarget}_{bindName};
DROP TRIGGER IF EXISTS do_not_insert_{modelSource}_with_invalid_{fieldSource}_{bindName};
DROP TRIGGER IF EXISTS do_not_update_{fieldSource}_on_{modelSource}_with_invalid_{fieldSource}_{bindName};"""
            query = template.format(
                bindName=bindName
                ,modelSource=bind['modelSource']
                ,fieldSource=bind['fieldSource']
                ,modelTarget=bind['modelTarget']
                ,fieldTarget=bind['fieldTarget']
            )
            self.bindingDict.pop(bindName)
            self.connection.executescript(query)
            return self
        else:
            raise NameError('Not exists the %s bind.' % name)


class Model:
    """An abstraction layer to manage sqlite3 database row-tables."""
    def __init__(self, tableName, connection):
        self.tableName = tableName
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.row_factory = self.connection.row_factory
        # In some cases is neccessary insert a row into database and then get
        # some fields of this new row. The "id" attribute contains the id of
        # that row.
        self.lastModelIdChanged = None

    def insert(self, **args):
        """Create a new row into self.tableName. Then fill them.
        Keyword arguments:
            **args -- arguments key-value with the fields values of row
        """
        query = 'INSERT INTO {tableName} ({fields}) VALUES ({placeholder})'
        sortedFields = collections.OrderedDict(sorted(args.items(), key=lambda t: t[0]))
        parameters = tuple(sortedFields.values())
        fields = sortedFields.keys()
        fields = ', '.join(fields)
        placeholder = ('?')*len(args)
        placeholder = ', '.join(placeholder)
        operation = query.format(
            tableName=self.tableName
            ,fields=fields
            ,placeholder=placeholder)
        return self._run_sql_query(operation, parameters)

    def update(self, fields, where, params):
        """Change the content of an existent row table.
        Keyword arguments:
            fields -- an dictionary with keys as fields, and values as data
            where -- an where clause with placeholder expression
            params -- the placeholder values"""
        query = 'UPDATE {tableName} SET {setClause} WHERE {whereClause}'
        sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
        fieldsParams = tuple(sortedFields.values())
        if isinstance(params, tuple) or isinstance(params, list):
            parameters = fieldsParams + params
        else:
            parameters = fieldsParams + (params,)
        keys = tuple(sortedFields.keys())
        setClause = '=?, '.join(keys) + '=?'
        operation = query.format(
            tableName=self.tableName
            ,setClause=setClause
            ,whereClause=where)
        return self._run_sql_query(operation, parameters)

    def get(self, fields=None, where=None, params=None, format=None, \
    separator=None, distinct=None):
        """Return a list with the falues of the sqlite3 query.
        get([fields] [,where, params] [,format [,separator]] [,distinct]) --
        Keyword arguments:
            fields -- the fields to get, if it is None return all fields
            where -- an where clause with placeholder expression
            params -- the placeholder values
            format -- the output format. The valid format are: strList, tupleList, dictList and default
                strList -- an list of str. Each value is separate for the 'separator' value
                tupleList -- an list of tuples with the vaules
                dictList -- an list of dicctionaries with keys as fields and values as data
                default -- an list of tuples with the vaules
                object -- a list of object
            separator -- an str that separates fields
            distinct -- if this is true, then the duplicate row are removed from the list"""
        # base template for the sql query
        query = 'SELECT{distinct}{fields}FROM{tableName}{where}'

        # set fields
        if fields:
            if isinstance(fields, str):
                _fields = (fields,)
            elif isinstance(fields, int):
                _fields = (repr(fields),)
            else:
                _fields = tuple(fields)
            _fields =' ' + ', '.join(_fields) + ' '
        else:
            _fields = ' * '

        # set WHERE clause
        # check that params is not None because params can be an
        # boolean type value
        if where and (params is not None):
            _where = ' WHERE ' + where
        else:
            if where and (params is None):
                raise TypeError("'params' argument is required")
            elif params and not where:
                raise TypeError("'where' argument is required")
            _where = ''

        # format the parameters
        parameters = self._format_parameters(params)

        # set format clause
        if format:
            validFormat = {'dictList', 'tupleList', 'default', 'strList', 'object'}
            if format not in validFormat:
                raise TypeError('"' + format + '" is an invalid type format')

        # render the sql query
        operation = query.format(
            fields=_fields
            ,distinct=' DISTINCT' if distinct else ''
            ,tableName=' ' + self.tableName
            ,where=_where)
        return self._run_sql_query(
            operation
            ,parameters
            ,format
            ,separator or '|'
            ,fetchAll=True)

    def has(self, where, params):
        """check if exists an row.
        Keyword arguments:
            where -- an where clause with placeholder expression
            params -- the placeholder values
        """
        # base template of the sqlquery
        query = 'SELECT * FROM{tableName}{where}'
        # format the parameters
        parameters = self._format_parameters(params)
        # fill the template
        operation = query.format(
            tableName=' ' + self.tableName
            ,where=' WHERE ' + where)
        idcount = self._run_sql_query(operation, parameters, fetchAll=True)
        return True if len(idcount) else False

    def remove(self, where, params):
        """Remove an row into database.
        Keyword arguments:
            where -- an where clause with placeholder expression
            params -- the placeholder values
        """
        query = 'DELETE FROM {tableName} WHERE {where}'
        if 'where':
            # format the parameters
            parameters = self._format_parameters(params)
            operation = query.format(
                tableName=self.tableName
                ,where=where)
        return self._run_sql_query(operation, parameters)

    def vacuum(self):
        """The VACUUM command rebuilds the entire database."""
        self.connection.execute('VACUUM')

    def save(self):
        """save changes into database"""
        self.connection.commit()

    # I set the property decorator because I dont want that the user change the
    # value of this attribute. Thas is for consistence reason.
    @property
    def maxItemIndex(self):
        """Return the max value of rowid."""
        query = 'SELECT max(rowid) FROM ' + self.tableName
        return self._run_sql_query(query, None, fetchAll=True)[0][0]

    def _dict_list(self, cursor, row):
        """make a dictionary with a name of column
        as key and column value as key value"""
        return {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }

    def _str_list(self, separator):
        """make an string with the value fields of
        rows separates by the separator value."""
        # BUG: the None value is represent as "None" string instead a void
        # value
        def inner(cursor, row):
            result = (
                str(row[idx]) for idx, col in enumerate(cursor.description)
            )
            return separator.join(result)
        return inner

    def _JavaScript_object(self, cursor, row):
        """return an object that alow attribute access by index or by dot"""
        _data = self._dict_list(cursor, row)
        return JavaScriptObject(_data)

    def _format_parameters(self, parameters):
        """Convert the parameters in a tuple of str or None value."""
        format = {
            "<class 'tuple'>": lambda p: p
            ,"<class 'list'>": lambda p: tuple(p)
            ,"<class 'NoneType'>": lambda p: p
            ,"<class 'str'>": lambda p: (p,)
            ,"<class 'int'>": lambda p: (repr(p),)
            ,"<class 'float'>": lambda p: (repr(p),)
            ,"<class 'bytes'>": lambda p: (repr(p),)
            ,"<class 'bool'>": lambda p: (p,)
            ,"<class 'datetime.date'>": lambda p: (p,)
            ,"<class 'datetime.datetime'>": lambda p: (p,)
        }
        try:
            return format[repr(type(parameters))](parameters)
        except:
            raise ValueError('the "params" field must be any of this type: "int", "float", "str", "bytes", "tuple", "bool", "list" or datetime.datetime.')

    def _run_sql_query(self, operation, parameters, format=None, \
            separator='|', fetchAll=None):
        """Execute an sql operation in the database"""
        if format:
            if format is 'dictList':
                self.connection.row_factory = self._dict_list
            elif format is 'strList':
                self.connection.row_factory = self._str_list(separator)
            elif format is 'object':
                self.connection.row_factory = self._JavaScript_object
            self.cursor = self.connection.cursor()
            self.connection.row_factory = self.row_factory
        else:
            self.cursor = self.connection.cursor()
        if parameters:
            self.cursor.execute(operation, parameters)
        else:
            self.cursor.execute(operation)
        # update the rowid of the last modified row.
        self.lastModelIdChanged = self.cursor.lastrowid
        return self.cursor.fetchall() if fetchAll else self


"""TODO:
- Remove the method chaining and replace this feature with the context manager
  in Collection and Model class.
- Remove the implicit save at exit and call save method in the __exit__()
  method of te context manager.
- View a way to represent the None value in the Model.get() method.
- Remove the OrderedDict and find a way to test all methods that use it.
- Investigate the use of ABC's.
- Find a better way to set forgein keys instead the Collection.bind() method.
- Remove the "None" string in the field is void.
"""