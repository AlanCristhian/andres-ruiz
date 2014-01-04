"""
Provides a class to handle tables within a database
sqlite3. But not handle the contents of the tables.
"""

import sqlite3
import collections

from framework.database import sqlite3Model


class Collection:
    """An abstraction layer to admin tables from sqlite3 databases.
    This class not manage the contents of the tables.
    """
    def __init__(self, dbpath, autocommit=True):
        self.dbpath = dbpath
        self.autocommit = autocommit
        self.type = {
            'int': 'INTEGER'
            ,'float': 'REAL'
            ,'str': 'TEXT'
            ,'bytes': 'BLOB'
            ,'prim': 'PRIMARY KEY'
            ,'intPrim': 'INTEGER PRIMARY KEY'
            ,'bool': 'BOOLEAN'
            # ,'None': 'NULL'
        }
        self.validTypes = set(self.type.keys())
        self.bindingDict = {}
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
        self.connection = sqlite3.connect(self.dbpath, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.execute('PRAGMA foreign_keys = ON')

        import atexit
        atexit.register(self._finalize)

    # Public methods

    def remove_fields(self, name, fields):
        """remove columns of the table"""
        query = self._remove_fields(name, fields)
        self.connection.executescript(query)
        return self

    def add_fields(self, name, fields):
        """add columns into an existing table"""
        fieldsTypes = set(fields.values())
        if not fieldsTypes.issubset(self.validTypes):
            self.validTypes = self.validTypes.difference(fieldsTypes)
            raise KeyError('"' + self.validTypes + '" is an invalid type of field.')
        query = self._add_fields(name, fields)
        if len(fields) == 1:
            self.connection.execute(query)
        else:
            self.connection.executescript(query)
        return self

    def path(self, dbpath=None):
        """Get an str and set dbpath as new database file and return the self
        instance. If not argument return a str with the path of database file.
        """
        if dbpath:
            self._set_database_path(dbpath)
            return self
        else:
            return self.dbpath

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
        query = self._create_model(name, fields)
        self.connection.execute(query)
        return self

    def remove(self, name):
        """Remove the table of the database and return the self instance.
        Keyword arguments:
            name -- the name of table to clear.
        """
        query = self._remove_model(name)
        self.connection.execute(query)
        return self

    def get(self, tableName):
        """Return an instance of the sqlite3Model class.
        Keyword arguments:
            tableName -- the name of the table binding to sqlite3Model class.
        """
        return sqlite3Model.Model(tableName, self.dbpath, self.connection, self.autocommit)

    def has(self, tableName): # 2 consult
        """Return True if the table name exists into the database.
        Else return False.
        Keyword arguments:
            name -- the table-name to check."""
        connection = sqlite3.connect(self.dbpath)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sqlite_master WHERE type=? AND name=?", ('table', tableName))
        tableCount = cursor.fetchall()
        cursor.close()
        connection.close()
        return True if len(tableCount) else False

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
        query = self._bind(bindName, modelSource, fieldSource, modelTarget, fieldTarget)
        self.connection.executescript(query)
        return self

    def unbind(self, bindName):
        """remove the triggers creates for bind.
        Keyword arguments:
            bindName -- the name of bind to remove
        """
        query = self._remove_bind(bindName)
        self.connection.executescript(query)
        return self

    def save(self):
        """save changes into database"""
        self.connection.commit()
        return self

    # def _get_key_by_value(self, mydict, value):
    #     for key, keyvalue in mydict.items():
    #         if keyvalue == value:
    #             return key

    # def set(self, name, fields):
    #     """Create an table into database"""
    #     fieldsTypes = set(fields.values())
    #     if not fieldsTypes.issubset(self.validTypes):
    #         self.validTypes = tuple(fieldsTypes.difference(self.validTypes))
    #         typeError = '"%s" is an invalid type of field.' % str(self.validTypes)
    #         currentType = self.validTypes[0]
    #         if isinstance(currentType, str):
    #             # assert self.has(modelTarget), KeyError(typeError)
    #             # assert self.get(modelTarget).has(fieldTarget), KeyError(typeError)
    #             try:
    #                 modelTarget, fieldTarget = currentType.split('.')
    #             except:
    #                 raise KeyError(typeError)
    #             try:
    #                 self._has_field(modelTarget, fieldTarget)
    #             except:
    #                 raise KeyError(typeError)
    #             foreignKey = self._get_key_by_value(fields, currentType)
    #             #set to NULL the datatype of the foreign key
    #             fields[foreignKey] = 'None'
    #             query = self._set(name, fields, foreignKey, modelTarget, fieldTarget)
    #         else:
    #             raise KeyError(typeError)
    #     else:
    #         query = self._create_model(name, fields)
    #     self.connection.execute(query)
    #     return self

    # def _has_field(self, model, field):
    #     """return the info of table"""
    #     query = 'SELECT {field} FROM {model}'.format(model=model, field=field)
    #     self.connection.execute(query)
    #     return True

    # def _set(self, name, fields, fieldSource, modelTarget, fieldTarget):
    #     """Return an string with sqlite3 query code to create a new table.
    #     Keyword arguments:
    #     name -- the model name
    #     fields -- an dict with name field has key and type value-has value
    #     """
    #     # template to create an table
    #     query = 'CREATE TABLE IF NOT EXISTS {name}({fields}, '\
    #         'FOREIGN KEY({fieldSource}) REFERENCES '\
    #         '{modelTarget}({fieldTarget}) ON INSERT CASCADE ON DELETE CASCADE ON UPDATE CASCADE)'
    #     # values sorted by key
    #     sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
    #     rows = (key + ' ' + self.type[sortedFields[key]] for key in sortedFields.keys())
    #     fields = ', '.join(rows)
    #     # fill the template
    #     operation = query.format(
    #         name=name
    #         ,fields=fields
    #         ,fieldSource=fieldSource
    #         ,fieldTarget=fieldTarget
    #         ,modelTarget=modelTarget
    #     )
    #     return operation

    def _remove_fields(self, name, fields):
        keys = self._fields(name)
        if isinstance(fields, str):
            keys.remove(fields)
        elif isinstance(fields, tuple) or isinstance(fields, list):
            for field in fields:
                keys.remove(field)
        else:
            raise TypeError('The "fields" parameter must be str, tuple or list type.')
        columns = ', '.join(keys)
        query = \
"""BEGIN TRANSACTION;
CREATE TEMPORARY TABLE table_backup({fields});
INSERT INTO table_backup SELECT {fields} FROM {name};
DROP TABLE {name};
CREATE TABLE {name}({fields});
INSERT INTO {name} SELECT {fields} FROM table_backup;
DROP TABLE table_backup;
COMMIT;
VACUUM;""".format(name=name, fields=columns)
        return query

    def _fields(self, name):
        """return the info of table"""
        query = 'SELECT * FROM {name}'.format(name=name)
        cursor = self.connection.execute(query)
        names = list(map(lambda x: x[0], cursor.description))
        return names

    def _add_fields(self, name, fields):
        query = 'ALTER TABLE {name} ADD COLUMN {fields};'
        # values sorted by key
        sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
        rows = (
            query.format(name=name, fields=key + ' ' + self.type[sortedFields[key]]) \
            for key in sortedFields.keys()
        )
        operation = '\n'.join(rows)
        return operation

    def _finalize(self):
        """commit the changes and close the database."""
        try:
            self.connection.commit()
            self.connection.close()
        except:
            pass

    def _set_database_path(self, dbpath):
        """Puth the dbpath value into self.dbpath property"""
        self.dbpath = dbpath

    def _create_model(self, name, fields):
        """Return an string with sqlite3 query code to create a new table.
        Keyword arguments:
        name -- the model name
        fields -- an dict with name field has key and type value-has value
        """
        # template to create an table
        query = 'CREATE TABLE IF NOT EXISTS {name} ({fields})'
        # values sorted by key
        sortedFields = collections.OrderedDict(sorted(fields.items(), key=lambda t: t[0]))
        rows = (key + ' ' + self.type[sortedFields[key]] for key in sortedFields.keys())
        fields = ', '.join(rows)
        # fill the template
        operation = query.format(
            name=name,
            fields=fields
        )
        return operation

    def _remove_model(self, name):
        """Return a string with an sqlite3 query code to delete the table.
        Keyword arguments:
        name -- the model name
        """
        query = 'DROP TABLE IF EXISTS {name}'.format(name=name)
        return query

    def _bind(self, bindName, modelSource, fieldSource, modelTarget, fieldTarget):
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
        query = template.format(
            bindName=bindName
            ,modelSource=modelSource
            ,fieldSource=fieldSource
            ,modelTarget=modelTarget
            ,fieldTarget=fieldTarget)
        return query

    def _remove_bind(self, bindName):
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
            return query
        else:
            return ''