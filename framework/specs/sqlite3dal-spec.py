import os
import sys
import unittest
import sqlite3
import datetime
import threading
from unittest.mock import Mock
import collections
import test
from framework import sqlite3dal


class QueryMakingTest(unittest.TestCase):
    """This class test that the query string making for each method has the
    correct sqlite3 query sintax.
    """
    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection._run_sql_query = Mock()
        self.collection._run_multiple_sql_query = Mock()
        self.model = self.collection.get('table_name')
        self.model._run_sql_query = Mock()

    def test_insert_query(self):
        """Should make the insert statement."""
        self.model.insert(id='1', key='value')
        expected =  ('INSERT INTO table_name (id, key) VALUES (?, ?)'
            ,('1', 'value'))
        self.model._run_sql_query.assert_called_with(*expected)

    def test_update_query(self):
        """Should make the update statement."""
        self.model.update(
            fields={
                'string': 'value',
                'int_number': 12345}
            ,where='id=?'
            ,params=1)
        expected =  ('UPDATE table_name SET int_number=?, string=? WHERE id=?'
            ,(12345, 'value', 1))
        self.model._run_sql_query.assert_called_with(*expected)

    def test_select_all_fields(self):
        """Should make a query that select all fields of the table."""
        self.model.get()
        expected = ('SELECT * FROM table_name', None, None, '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_select_many_fields(self):
        self.model.get(fields=('id', 'key'))
        expected = ('SELECT id, key FROM table_name', None, None, '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_select_one_field(self):
        self.model.get(fields='id')
        expected = ('SELECT id FROM table_name', None, None, '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_select_fields_with_where_clause(self):
        """Should select the fields that satisfy the condition in the where
        keyword.
        """
        self.model.get(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value'))
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?'
            ,('1', 'value'), None, '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_select_with_distinct_clause(self):
        """Should not return repeated data."""
        self.model.get(fields='id', distinct=True)
        expected = ('SELECT DISTINCT id FROM table_name', None, None, '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_should_return_a_dictList_parameter(self):
        self.model.get(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='dictList')
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?'
            ,('1', 'value'), 'dictList', '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_should_return_a_strList_parameter(self):
        self.model.get(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?'
            ,('1', 'value'), 'strList', '|')
        self.model._run_sql_query.assert_called_with(*expected, fetchAll=True)

    def test_should_get_many_fields_that_satisfy_the_condition(self):
        self.model.get(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        self.model._run_sql_query.assert_called_with(
            'SELECT id, key FROM table_name WHERE id=? and key=?'
            ,('1', 'value')
            ,'strList'
            ,'|'
            ,fetchAll=True)

    def test_should_get_all_fields_that_satisfy_the_condition(self):
        self.model.get(
            where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        self.model._run_sql_query.assert_called_with(
            'SELECT * FROM table_name WHERE id=? and key=?'
            ,('1', 'value')
            ,'strList'
            ,'|'
            ,fetchAll=True)

    def test_should_get_the_table_with_an_specific_rowid(self):
        self.model.get(
            fields='rowid'
            ,where='rowid=?'
            ,params='1')
        self.model._run_sql_query.assert_called_with(
            'SELECT rowid FROM table_name WHERE rowid=?'
            ,('1',)
            ,None
            ,'|'
            ,fetchAll=True)

    def test_should_get_make_a_query_that_get_the_max_rowid(self):
        self.model._run_sql_query = Mock(return_value=[(1,)])
        self.model.maxItemIndex
        self.model._run_sql_query.assert_called_with(
            'SELECT max(rowid) FROM table_name', None, fetchAll=True)

    def test_should_return_an_delete_query_with_one_parameter(self):
        self.model.remove(where='id=?', params='1')
        expected = ('DELETE FROM table_name WHERE id=?', ('1',))
        self.model._run_sql_query.assert_called_with(*expected)

    def test_should_return_an_delete_query_with_many_parameters(self):
        self.model.remove(where='id=? and key=?', params=('1', 'value'))
        expected = ('DELETE FROM table_name WHERE id=? and key=?'
            ,('1', 'value'))
        self.model._run_sql_query.assert_called_with(*expected)

    def test_should_call_delete_and_run_sql_query(self):
        self.model.remove(where='id=?', params='1')
        self.model._run_sql_query.assert_called_with(
            'DELETE FROM table_name WHERE id=?', ('1',))

    def test_should_call_has_item_method(self):
        self.model._run_sql_query = Mock(return_value=[])
        self.model.has(where='id=?', params='1')
        self.model._run_sql_query.assert_called_with(
            'SELECT * FROM table_name WHERE id=?', ('1',) , fetchAll=True)

    def testh_should_call_vacuum_method(self):
        self.model.connection = Mock()
        self.model.connection.execute = Mock()
        self.model.vacuum()
        self.model.connection.execute.assert_called_with('VACUUM')

    def test_should_raise_error_if_missing_params_argument(self):
        self.assertRaises(TypeError, self.model.get,
            fields=('id', 'key')
            ,where='id=?')

    def test_should_raise_error_if_missing_where_argument(self):
        self.assertRaises(TypeError, self.model.get,
            fields=('id', 'key')
            ,params=('1', 'value'))

    def test_should_raise_error_if_params_get_an_invalid_type_argument(self):
        self.assertRaises(TypeError, self.model.get,
            fields=('id', 'key')
            ,params={'id': '1', 'key': 'value'})

    def test_should_raise_error_if_set_an_invalid_argument(self):
        self.assertRaises(TypeError, self.model.remove,
            invalidArg='an invalid argument')

    def test_should_raise_error_if_set_an_not_valid_format_string(self):
        self.assertRaises(TypeError, self.model.get,
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='invalid format')


class MethodsBehaviorTest(unittest.TestCase):
    """Check that spec of behavior espected in all public method is correct.
    """
    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='model_name'
            ,fields={
                'id': 'intPrim'
                ,'texto': 'str'
                ,'numero': 'int'})
        self.model = self.collection.get('model_name')
        self.model\
            .insert(
                texto='primer texto'
                ,numero=111111111)\
            .insert(
                texto='segundo texto'
                ,numero=222222222)\
            .insert(
                texto='tercer texto'
                ,numero=333333333)

    def test_should_cal_set_an_update_query(self):
        self.model._run_sql_query = Mock()

        obtained = self.model.update(
            fields={'numero': 444444444}
            ,where='id=?'
            ,params=1)
        self.model._run_sql_query.assert_called_with(
            'UPDATE model_name SET numero=? WHERE id=?'
            ,(444444444, 1)
            )

    def test_should_chainin_the_methods_result(self):
        model = self.collection.get('model_name')
        model\
            .insert(
                texto='primer texto'
                ,numero=111111111
            )\
            .insert(
                texto='segundo texto'
                ,numero=222222222
            )\
            .insert(
                texto='tercer texto'
                ,numero=333333333
            )\
            .insert(
                texto=None
                ,numero=None
            )\
            .update(
                fields={'numero': 444444444}
                ,where='id=?'
                ,params=1
            )\
            .remove(
                where='rowid=?'
                ,params=('2',)
            )\
            .get()

    def test_max_rowid_in_memory(self):
        """As the setUp method insert 3 rows in the database buth all test case
        methods in this file shared the same database (:memory:) the
        maxItemIndex should be major to 3.
        """
        self.model = self.collection.get('model_name')
        self.assertTrue(self.model.maxItemIndex >= 3)

    def test_id_updating_attribute(self):
        """Should update the "id" attribute with the last row id consulted.
        This is the same that sqlite3.Cursor.lastrowid attribute.
        """
        model = self.collection.get('model_name')
        model.insert(
            texto='primer texto'
            ,numero=111111111
        )
        # The default value of the id attribute is None. If after the insert
        # operation in the id type is int then de id attribute is updated.
        self.assertIsInstance(model.lastModelIdChanged, int)


class ConnectionSpecificationTest(unittest.TestCase):
    def tearDown(self):
        """Remove all files created in the testing.
        """
        for i in range(1, 11):
            try:
                os.remove('test_different_connection' + str(i) + '.db')
                os.remove('test_same_connection' + str(i) + '.db')
            except:
                pass
        try:
            os.remove('test_different_connection.db')
            os.remove('test_same_connection.db')
        except:
            pass

    def test_same_connection_on_different_threads(self):
        """All instances of sqlite3dal.Connection should be the same instance
        if the database path is equal.
        """
        initial_connection = sqlite3dal.Connection('test_same_connection.db')
        def worker():
            current_connection = sqlite3dal.Connection(
                'test_same_connection.db')
            self.assertIs(current_connection, initial_connection)
        for thread in range(10):
            threading.Thread(target=worker).start()

    def test_different_connection_on_different_threads(self):
        """All instances of sqlite3dal.Connection should be the differents
        object if the database path is different on each invocation.
        """
        initial_connection = sqlite3dal.Connection(
            'test_different_connection.db')
        counter = 0
        def worker():
            nonlocal counter
            counter += 1
            current_connection = sqlite3dal.Connection(
                'test_different_connection' + str(counter) + '.db')
            self.assertIsNot(
                current_connection, initial_connection)
        for thread in range(10):
            threading.Thread(target=worker).start()


class FormatResultsTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='model_name'
            ,fields={
                'id': 'intPrim'
                ,'texto': 'str'
                ,'numero': 'int'})
        self.model = self.collection.get('model_name')
        self.model\
            .insert(
                texto='primer texto'
                ,numero=111111111)\
            .insert(
                texto='segundo texto'
                ,numero=222222222)

    def tearDown(self):
        self.collection.remove('model_name')

    def test_should_get_result_in_strList_format(self):
        obtained = self.model.get(format='strList')
        expected = ['1|111111111|primer texto', '2|222222222|segundo texto']
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_default_format(self):
        obtained = self.model.get(format='default')
        expected = [(1, 111111111, 'primer texto')
        , (2, 222222222, 'segundo texto')]
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_tupleList_format(self):
        obtained = self.model.get(format='tupleList')
        expected = [(1, 111111111, 'primer texto')
        , (2, 222222222, 'segundo texto')]
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_dictList_format(self):
        obtained = self.model.get(format='dictList')
        expected = [{'texto': 'primer texto', 'id': 1, 'numero': 111111111}
        , {'texto': 'segundo texto', 'id': 2, 'numero': 222222222}]
        self.assertEqual(expected, obtained)


    def test_should_get_result_in_strList_format(self):
        data = self.model.get(format='object')[0]
        self.assertTrue(hasattr(data, 'texto'))
        self.assertTrue(hasattr(data, 'id'))
        self.assertTrue(hasattr(data, 'numero'))


    def test_should_check_if_exists_a_row(self):
        obtained1 = self.model.has(where='id=?', params='1')
        self.assertEqual(obtained1, True)

        obtained2 = self.model.has(where='id=?', params='2')
        self.assertEqual(obtained2, True)

        obtained3 = self.model.has(where='id=?', params='3')
        self.assertEqual(obtained3, False)


class ModelBooleanTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='row_test'
            ,fields={
                'id': 'intPrim'
                ,'booleano': 'bool'})
        self.model = self.collection.get('row_test')
        self.model\
            .insert(booleano=False)\
            .insert(booleano=False)\
            .insert(booleano=True)\
            .insert(booleano=True)

    def tearDown(self):
        self.collection.remove('row_test')

    def test_should_get_the_False_values(self):
        obtained = self.model.get(
            where='booleano=?'
            ,params=False
            ,format='dictList')
        expected = [
            {'id': 1, 'booleano': False}
            ,{'id': 2, 'booleano': False}
        ]
        self.assertEqual(obtained, expected)

    def test_should_get_the_True_values(self):
        obtained = self.model.get(
            where='booleano=?'
            ,params=True
            ,format='dictList')
        expected = [
            {'id': 3, 'booleano': True}
            ,{'id': 4, 'booleano': True}
        ]
        self.assertEqual(obtained, expected)

    def test_should_update_the_False_values(self):
        self.model.update(
            fields={'booleano': True}
            ,where='booleano=?'
            ,params=False)
        obtained = self.model.get(
            where='booleano=?'
            ,params=True
            ,format='dictList')
        expected = [
            {'booleano': True, 'id': 1}
            ,{'booleano': True, 'id': 2}
            ,{'booleano': True, 'id': 3}
            ,{'booleano': True, 'id': 4}
        ]
        self.assertEqual(obtained, expected)

    def test_should_update_the_True_values(self):
        self.model.update(
            fields={'booleano': False}
            ,where='booleano=?'
            ,params=True)
        obtained = self.model.get(
            where='booleano=?'
            ,params=False
            ,format='dictList')
        expected = [
            {'id': 1, 'booleano': False}
            ,{'id': 2, 'booleano': False}
            ,{'id': 3, 'booleano': False}
            ,{'id': 4, 'booleano': False}
        ]
        self.assertEqual(obtained, expected)

    def test_should_remove_all_False_row(self):
        self.model.remove(
                where='booleano=?'
                ,params=False)
        obtained = self.model.get(format='dictList')
        expected = [
            {'id': 3, 'booleano': True}
            ,{'id': 4, 'booleano': True}
        ]
        self.assertEqual(obtained, expected)

    def test_should_remove_all_True_row(self):
        obtained = self.model\
            .remove(
                where='booleano=?'
                ,params=True)\
            .get(format='dictList')
        expected = [
            {'id': 1, 'booleano': False}
            ,{'id': 2, 'booleano': False}
        ]
        self.assertEqual(obtained, expected)


class CollectionComponentTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection._set_database_path = Mock()

    def test_should_call_set_database_path_and_return_self(self):
        expected = 'another/path'
        self.collection.path('another/path')
        self.assertEqual(self.collection.dbpath, expected)

    def test_should_return_database_path(self):
        expected = self.collection.path()
        self.assertEqual(':memory:', expected)

    def test_create_sentence_with_all_types(self):
        """Should make a query with all types suported."""
        self.collection.create(name='test', fields={
            'bool_key':         'bool',
            'byte_key':         'bytes',
            'date_key':         'date',
            'datetime_key':     'datetime',
            'real_key':         'float',
            'integer_key':      'int',
            'int_primary_key':  'intPrim',
            'primary_key':      'prim',
            'string_key':       'str'})
        self.collection.connection.execute.assert_called_with(
            'CREATE TABLE IF NOT EXISTS test ('\
                'bool_key BOOLEAN'\
                ', byte_key BLOB'\
                ', date_key DATE'\
                ', datetime_key TIMESTAMP'\
                ', int_primary_key INTEGER PRIMARY KEY'\
                ', integer_key INTEGER'\
                ', primary_key PRIMARY KEY'\
                ', real_key REAL'\
                ', string_key TEXT'\
            ')'
        )

    def test_should_make_an_delete_table_sentence(self):
        self.collection.remove(name ='test_table')
        expected = 'DROP TABLE IF EXISTS test_table'
        self.collection.connection.execute.assert_called_with(
            expected)

    def test_should_raise_an_error_for_an_ivalid_argument(self):
        self.assertRaises(TypeError, self.collection.create,
            name ='test_table',
            fields = {
                'id': 'int'
                ,'key': 'str'}
            ,error='an invalid key')

    def test_should_raise_an_error_for_an_invalid_table_name(self):
        self.assertRaises(TypeError, self.collection.remove, fields='test_table')

    def test_should_raise_an_error_for_an_Null_table_name(self):
        self.assertRaises(TypeError, self.collection.remove)

    def test_should_raise_an_error_for_fields_required(self):
        self.assertRaises(TypeError, self.collection.create, 'test_table')

    def test_should_be_raise_an_error_for_invalid_type_field(self):
        self.assertRaises(KeyError, self.collection.create,
            name ='test_table',
            fields = {
                'id': 'int'
                ,'key': 'invalidType'})

    def test_should_call_remove_model_and_run_sql_query(self):
        self.collection.remove('test')
        self.collection.connection.execute.assert_called_with('DROP TABLE IF EXISTS test')

    def test_should_convert_bool_to_BOOLEAN(self):
        self.collection.create(
            name='bool_test'
            ,fields={
                'id': 'prim'
                ,'boolean_key': 'bool'})
        expected = 'CREATE TABLE IF NOT EXISTS bool_test (boolean_key BOOLEAN, id PRIMARY KEY)'
        self.collection.connection.execute.assert_called_with(
            expected)


class CollectionServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
                name='test',
                fields = {
                    'id': 'int'
                    ,'key': 'str'})

    def test_should_table_not_exist(self):
        doNotHasTable = self.collection.has('any_table')
        self.assertEqual(doNotHasTable, False)

    def test_should_exist_the_table(self):
        hasTable = self.collection.has('test')
        self.assertEqual(hasTable, True)

    def test_should_get_fields(self):
        obtained = self.collection._fields('test').sort()
        expected = ['id', 'key'].sort()
        self.assertEqual(obtained, expected)


class CollectionTriggersTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.connection = Mock()
        self.collection.connection.executescript = Mock()
        self.collection.create(
            name='articles'
            ,fields={
                'id': 'intPrim'
                ,'article_name': 'str'})
        self.collection.create(
            name='images'
            ,fields={
                'id': 'intPrim'
                ,'article_name': 'str'})
        self.collection.bind(
            bindName='test_bind'
            ,modelSource='images'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name')

    def test_should_auto_create_trigger_to_forgein_key(self):
        self.collection.connection.executescript.assert_called_with(
"""CREATE TRIGGER IF NOT EXISTS update_article_name_on_images_when_update_article_name_in_articles_test_bind
    AFTER UPDATE ON articles
        FOR EACH ROW BEGIN
            UPDATE images SET article_name = NEW.article_name WHERE images.article_name = OLD.article_name;
        END;

CREATE TRIGGER IF NOT EXISTS delete_images_when_delete_article_name_from_articles_test_bind
    BEFORE DELETE ON articles
        FOR EACH ROW BEGIN
            DELETE FROM images WHERE images.article_name = OLD.article_name;
        END;

CREATE TRIGGER IF NOT EXISTS do_not_insert_images_with_invalid_article_name_test_bind
    BEFORE INSERT ON images
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't insert the register")
            WHERE (SELECT article_name FROM articles WHERE articles.article_name=NEW.article_name) IS NULL;
        END;

CREATE TRIGGER IF NOT EXISTS do_not_update_article_name_on_images_with_invalid_article_name_test_bind
    BEFORE UPDATE ON images 
        FOR EACH ROW BEGIN
            SELECT RAISE (ROLLBACK, "Can't update the register")
            WHERE (SELECT article_name FROM articles WHERE articles.article_name=NEW.article_name) IS NULL;
        END;""")

    def test_should_remove_triggers(self):
        self.collection.unbind(bindName='test_bind')
        self.collection.connection.executescript.assert_called_with(
"""DROP TRIGGER IF EXISTS update_article_name_on_images_when_update_article_name_in_articles_test_bind;
DROP TRIGGER IF EXISTS delete_images_when_delete_article_name_from_articles_test_bind;
DROP TRIGGER IF EXISTS do_not_insert_images_with_invalid_article_name_test_bind;
DROP TRIGGER IF EXISTS do_not_update_article_name_on_images_with_invalid_article_name_test_bind;""")

    def test_not_exists_the_bind(self):
        self.assertRaises(
            NameError
            ,self.collection.unbind
            ,bindName='not_valid_name_bind')


class TriggersIntegrityTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection\
            .create(name='images', fields={
                    'id': 'intPrim'
                    ,'description': 'str'
                    ,'article_name': 'str'})\
            .create(name='articles', fields={
                    'id': 'intPrim'
                    ,'description': 'str'
                    ,'article_name': 'str'})
        self.articles = self.collection.get('articles')
        self.images = self.collection.get('images')
        self.articles.insert(article_name='first_article', description='An article description')
        self.articles.insert(article_name='second_article', description='Another article description')
        self.images.insert(article_name='first_article', description='first image')
        self.images.insert(article_name='first_article', description='second image')
        self.images.insert(article_name='second_article', description='first image in second_article')
        self.images.insert(article_name='second_article', description='second image in second_article')
        self.collection.bind(
            bindName='test_bind'
            ,modelSource='images'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name')

    def tearDown(self):
        self.collection.remove('images').remove('articles')

    def test_should_not_be_create_trigger(self):
        self.collection.remove('articles').remove('images')
        self.assertRaises(sqlite3.OperationalError, self.collection.bind,
            bindName='test_bind'
            ,modelSource='images'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name')

    def test_should_raise_error_when_try_INSERT_with_wrong_table_name(self):
        self.assertRaises(sqlite3.IntegrityError, self.images.insert, article_name='third_article', description='invalid article name')

    def test_should_not_exists_the_table(self):
        self.assertFalse(self.images.has(where='article_name=?', params='third_article'))

    def test_should_raise_error_when_try_UPDATE_with_wrong_table_name(self):
        self.assertRaises(sqlite3.IntegrityError, self.images.update, fields={'article_name': 'third_article'}, where='id=?', params=1)

    def test_should_update_all_images(self):
        self.articles.update(
            fields={'article_name': 'article_1'}
            ,where='id=?'
            ,params=1)
        obtained = self.images.get(where='article_name=?', params='article_1')
        expected = [('article_1', 'first image', 1), ('article_1', 'second image', 2)]
        self.assertEqual(expected, obtained)

    def test_should_remove_all_images(self):
        self.articles.remove(where='article_name=?', params='article_1')
        obtained = self.images.get(where='article_name=?', params='article_1')
        expected = []
        self.assertEqual(expected, obtained)

    def test_should_get_only_the_rest_images(self):
        self.articles.remove(where='article_name=?', params='article_1')
        obtained = self.images.get(where='article_name=?', params='second_article')
        expected = [('second_article', 'first image in second_article', 3), ('second_article', 'second image in second_article', 4)]
        self.assertEqual(expected, obtained)


class CollectionBooleanTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='bool_test'
            ,fields={
                'id':           'prim'
                ,'boolean_key': 'bool'})

    def tearDown(self):
        self.collection.remove('bool_test')

    def test_should_set_boolean_value(self):
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=True)

    def test_should_get_boolean_value_as_True(self):
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=True)
        obtained = self.boolModel.get(
            fields='boolean_key'
            ,format='dictList')[0]
        expected = {'boolean_key': True}
        self.assertEqual(expected, obtained)

    def test_should_get_boolean_value_as_False(self):
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=False)
        obtained = self.boolModel.get(
            fields='boolean_key'
            ,format='dictList')[0]
        expected = {'boolean_key': False}
        self.assertEqual(expected, obtained)

    def test_should_be_an_instance_of_boolean_class(self):
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=False)
        false_result = self.boolModel.get(
            fields='boolean_key'
            ,where='boolean_key=?'
            ,params=(False,)
            ,format='dictList')[0]
        self.assertIsInstance(false_result['boolean_key'], bool)


class CollectionDateTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='date_test'
            ,fields={
                'id':        'prim'
                ,'date_key': 'date'})

    def tearDown(self):
        self.collection.remove('date_test')

    def test_set_date_value(self):
        """Should insert a date type value without raise any error.
        """
        self.dateModel = self.collection.get('date_test')
        self.dateModel.insert(date_key=datetime.date.today())

    def test_get_date_value(self):
        """Should get and date type value.
        """
        self.dateModel = self.collection.get('date_test')
        self.dateModel.insert(date_key=datetime.date.today())
        obtained = self.dateModel.get(
            fields='date_key'
            ,format='dictList')[0]
        expected = {'date_key': datetime.date.today()}
        self.assertEqual(expected, obtained)

    def test_be_an_instance_of_date_class(self):
        self.dateModel = self.collection.get('date_test')
        self.dateModel.insert(date_key=datetime.date.today())
        obtained = self.dateModel.get(
            fields='date_key'
            ,format='dictList')[0]
        self.assertIsInstance(obtained['date_key'], datetime.date)


class CollectionDatetimeTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(
            name='datetime_test'
            ,fields={
                'id':            'prim'
                ,'datetime_key': 'datetime'})
        self.datetime = datetime.datetime.now()

    def tearDown(self):
        self.collection.remove('datetime_test')

    def test_set_datetime_value(self):
        """Should insert a datetime type value without raise any error.
        """
        self.datetimeModel = self.collection.get('datetime_test')
        self.datetimeModel.insert(datetime_key=self.datetime)

    def test_get_datetime_value(self):
        """Should get and date type value.
        """
        self.datetimeModel = self.collection.get('datetime_test')
        self.datetimeModel.insert(datetime_key=self.datetime)
        obtained = self.datetimeModel.get(
            fields='datetime_key'
            ,format='dictList')[0]
        expected = {'datetime_key': self.datetime}
        self.assertEqual(expected, obtained)

    def test_be_an_instance_of_date_class(self):
        self.datetimeModel = self.collection.get('datetime_test')
        self.datetimeModel.insert(datetime_key=self.datetime)
        obtained = self.datetimeModel.get(
            fields='datetime_key'
            ,format='dictList')[0]
        self.assertIsInstance(obtained['datetime_key'], datetime.datetime)


class TableModificationTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3dal.Collection(':memory:')
        self.collection.create(name='test_table', fields={
            'id': 'prim'
            ,'string': 'str'
            ,'boolean': 'bool'
            ,'integer': 'int'})
        self.table = self.collection.get('test_table')

    def tearDown(self):
        self.collection\
            .remove('test_table')\
            .remove('my_table')

    def test_should_make_a_query_that_add_one_field(self):
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection.add_fields(name='test_table', fields={'real_key': 'float'})
        expected = 'ALTER TABLE test_table ADD COLUMN real_key REAL'
        self.collection.connection.execute.assert_called_with(
            expected)

    def test_add_many_fields_query(self):
        """Should make a query that add many operations to one query.
        """
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection.add_fields(name='test_table', fields={
            'real_key': 'float'
            ,'str_key': 'str'})
        expected =  "ALTER TABLE test_table ADD COLUMN real_key REAL;\n"\
                    "ALTER TABLE test_table ADD COLUMN str_key TEXT"
        self.collection.connection.executescript.assert_called_with(
            expected)

    def test_should_call_add_fields_method(self):
        self.collection.add_fields = Mock()
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection.add_fields('table_name', {'real_key': 'float'})
        self.collection.add_fields.assert_called_with('table_name', {'real_key': 'float'})

    def test_should_add_fields(self):
        self.collection.create(name='table_name', fields={
            'int_key': 'int'
            ,'str_key': 'str'})
        self.collection.add_fields(name='table_name', fields={
            'float_key': 'float'
            ,'bool_key': 'bool'})
        obtained = self.collection._fields('table_name').sort()
        expected = ['int_key', 'str_key', 'float_key', 'bool_key'].sort()
        self.assertEqual(expected, obtained)

    def test_should_make_a_query_that_remove_one_field(self):
        self.collection.create('my_table', {'a': 'int', 'b': 'str', 'c': 'float'})
        self.collection.remove_fields(name='my_table', fields='c')
        expected = \
"""BEGIN TRANSACTION;
CREATE TEMPORARY TABLE table_backup(a, b);
INSERT INTO table_backup SELECT a, b FROM my_table;
DROP TABLE my_table;
CREATE TABLE my_table(a, b);
INSERT INTO my_table SELECT a, b FROM table_backup;
DROP TABLE table_backup;
COMMIT;
VACUUM;"""
        self.assertEqual(expected, self.collection._result)


    def test_should_make_a_query_that_remove_many_fields(self):
        self.collection.create('my_table', {'a': 'int', 'b': 'str', 'c': 'float', 'd': 'bool'})
        self.collection.remove_fields(name='my_table', fields=('c', 'd'))
        expected = \
"""BEGIN TRANSACTION;
CREATE TEMPORARY TABLE table_backup(a, b);
INSERT INTO table_backup SELECT a, b FROM my_table;
DROP TABLE my_table;
CREATE TABLE my_table(a, b);
INSERT INTO my_table SELECT a, b FROM table_backup;
DROP TABLE table_backup;
COMMIT;
VACUUM;"""
        self.assertEqual(expected, self.collection._result)

    def test_should_remove_any_fields(self):
        self.collection.remove_fields('test_table', ('boolean', 'integer'))
        obtained = self.collection._fields('test_table').sort()
        expected = ['id', 'string'].sort()
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()