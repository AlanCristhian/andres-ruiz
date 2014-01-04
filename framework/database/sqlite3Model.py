"""Provide a class to manage table rows on sqlite3 databases"""

import re
import collections


class JavaScriptObject(dict):
    """The attribute can be referenced by indexing (e.g. d[name])
    or by directly using the dot (.) operator (e.g. d.name)."""
    def __init__(self, *args, **kwargs):
        self.update(*args)
        self.update(**kwargs)

    def __getattr__(self, name):
        return self[name]
            
    def __setattr__(self, name, value):
        self[name] = value


class Model:
    """An abstraction layer to manage sqlite3 database row-tables."""
    def __init__(self, tableName, dbPath, connection, autocommit):
        self.tableName = tableName
        self.dbPath = dbPath
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.row_factory = self.connection.row_factory
        self.autocommit = autocommit

    def insert(self, **args):
        """Create a new row into self.tableName. Then fill them.
        Keyword arguments:
            **args -- arguments key-value with the fields values of row
        """
        result = self._insert(**args)
        return self._run_sql_query(
            operation=result[0]
            ,parameters=result[1]
            ,commit=True)

    def update(self, fields, where, params):
        """Change the content of an existent row table.
        Keyword arguments:
            fields -- an dictionary with keys as fields, and values as data
            where -- an where clause with placeholder expression
            params -- the placeholder values"""
        # result = self._update(**args)
        result = self._update(fields, where, params)
        return self._run_sql_query(
            operation=result[0]
            ,parameters=result[1]
            ,commit=True)

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
            separator -- an str that separates fields
            distinct -- if this is true, then the duplicate row are removed from the list"""
        result = self._select(fields, where, params, format, separator,\
            distinct)
        return self._run_sql_query(
            operation=result[0]
            ,parameters=result[1]
            ,format=result[2]
            ,separator=result[3]
            ,fetchAll=True)

    def remove(self, where, params):
        """Remove an row into database.
        Keyword arguments:
            where -- an where clause with placeholder expression
            params -- the placeholder values
            """
        result = self._delete(where, params)
        return self._run_sql_query(
            operation=result[0]
            ,parameters=result[1]
            ,commit=True)

    def has(self, where, params):
        """check if exists an row.
        Keyword arguments:
            where -- an where clause with placeholder expression
            params -- the placeholder values"""
        result = self._has_item(where, params)
        idcount = self._run_sql_query(
            operation=result[0] 
            ,parameters=result[1] 
            ,fetchAll=True)
        return True if len(idcount) else False

    def vacuum(self):
        """The VACUUM command rebuilds the entire database."""
        self._run_sql_query(operation='VACUUM', commit=True)

    def save(self):
        """save changes into database"""
        self.connection.commit()

    def _insert(self, **args):
        """Return the sql operation for insert data in the table."""
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
        return operation, parameters

    def _update(self, fields, where, params):
        """Return the sql operation for update the data in the table."""
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
        return operation, parameters

    def _select(self, fields=None, where=None, params=None, format=None, \
    separator=None, distinct=None):
        """return the sql operation for get the values"""
        # base template for the sql query
        query = 'SELECT{distinct}{fields}FROM{tableName}{where}'

        # default values of clauses
        _distinct = ''
        _where = ''
        _separator = separator or '|'

        # set fields
        if fields:
            if isinstance(fields, str):
                _fields = (fields,)
            elif isinstance(fields, int):
                _fields = (str(fields),)
            else:
                _fields = tuple(fields)
            _fields =' ' + ', '.join(_fields) + ' '
        else:
            _fields = ' * '

        # set WHERE clause
        if where and (params is not None):
            _where = ' WHERE ' + where
        else:
            if where and (params is None):
                raise TypeError("'params' argument is required")
            elif params and not where:
                raise TypeError("'where' argument is required")

        # set distinct cluse
        if distinct:
            _distinct = ' DISTINCT'

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
            ,distinct=_distinct
            ,tableName=' ' + self.tableName
            ,where=_where)
        return operation, parameters, format, _separator

    def _has_item(self, where, params):
        """return the sql operation for get the values"""
        # base template of the sqlquery
        query = 'SELECT * FROM{tableName}{where}'
        # set where clause
        _where = ' WHERE ' + where
        # format the parameters
        parameters = self._format_parameters(params)
        # fill the template
        operation = query.format(
            tableName=' ' + self.tableName
            ,where=_where)
        return operation, parameters,

    def _delete(self, where=None, params=None):
        """return the sql operation for delete a row in table"""
        query = 'DELETE FROM {tableName} WHERE {where}'
        if 'where':
            # format the parameters
            parameters = self._format_parameters(params)
            operation = query.format(
                tableName=self.tableName
                ,where=where)
        return operation, parameters

    def _dict_list(self, cursor, row):
        """make a dictionary with a name of column
        as key and column value as key value"""
        return {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }

    def _str_list(self, separator):
        """make an string with the value fields of
        rows separates by the separator value."""
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
            ,"<class 'int'>": lambda p: (str(p),)
            ,"<class 'float'>": lambda p: (str(p),)
            ,"<class 'bytes'>": lambda p: (str(p),)
            ,"<class 'bool'>": lambda p: (p,)
        }
        try:
            return format[str(type(parameters))](parameters)
        except Exception as e:
            raise ValueError('the "params" field must be any of this type: "int", "float", "str", "bytes", "tuple", "bool" or "list".')

    def _run_sql_query(self, operation, parameters, format=None, \
    separator='|', fetchAll=None, commit=None):
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
        try:
            if parameters:
                self.cursor.execute(operation, parameters)
            else:
                self.cursor.execute(operation)
            if fetchAll:
                queryResult = self.cursor.fetchall()
            else:
                queryResult = self
            if commit and self.autocommit:
                self.connection.commit()
            return queryResult
        except Exception as e:
            raise e