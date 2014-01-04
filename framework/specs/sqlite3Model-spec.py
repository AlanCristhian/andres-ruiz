import os
import sys
import unittest

from unittest.mock import Mock

oldDirectory = os.getcwd()
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from database import sqlite3Collection
from database import sqlite3Model
os.chdir(oldDirectory)


class ModelComponentTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection(':memory:')
        self.collection._run_sql_query = Mock()
        self.collection._run_multiple_sql_query = Mock()
        self.model = self.collection.get('table_name')
        self.model._run_sql_query = Mock()

    def test_should_call_insert_method(self):
        self.model._insert = Mock(return_value='test')
        self.model.insert(fields='test')
        self.model._insert.assert_called_with(fields='test')

    def test_should_return_an_insert_query(self):
        obtained = self.model._insert(id='1', key='value')
        expected = ('INSERT INTO table_name (id, key) VALUES (?, ?)', ('1', 'value'))
        self.assertEqual(expected, obtained)

    def test_should_return_an_update_query(self):
        obtained = self.model._update(
            fields={
                'string': 'value',
                'int_number': 12345}
            ,where='id=?'
            ,params=1)
        expected = ('UPDATE table_name SET int_number=?, string=? WHERE id=?', (12345, 'value', 1))
        self.assertEqual(expected, obtained)

    def test_should_call_insert_and_run_sql_query(self):
        self.model.insert(id='1', key='value')
        operation ='INSERT INTO table_name (id, key) VALUES (?, ?)'
        parameters = ('1', 'value')
        self.model._run_sql_query.assert_called_with(operation=operation, parameters=parameters, commit=True)

    def test_should_select_all_fields(self):
        obtained = self.model._select()
        expected = ('SELECT * FROM table_name', None, None, '|')
        self.assertEqual(expected, obtained)

    def test_should_select_many_fields(self):
        obtained = self.model._select(fields=('id', 'key'))
        expected = ('SELECT id, key FROM table_name', None, None, '|')
        self.assertEqual(expected, obtained)

    def test_should_select_one_field(self):
        obtained = self.model._select(fields='id')
        expected = ('SELECT id FROM table_name', None, None, '|')
        self.assertEqual(expected, obtained)

    def test_should_select_the_fields_that_satisfy_the_condition(self):
        obtained = self.model._select(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value'))
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?', ('1', 'value'), None, '|')
        self.assertEqual(expected, obtained)

    def test_should_not_return_repeated_data(self):
        obtained = self.model._select(fields='id', distinct=True)
        expected = ('SELECT DISTINCT id FROM table_name', None, None, '|')
        self.assertEqual(expected, obtained)

    def test_should_return_a_dictList_parameter(self):
        obtained = self.model._select(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='dictList')
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?', ('1', 'value'), 'dictList', '|')
        self.assertEqual(expected, obtained)

    def test_should_return_a_strList_parameter(self):
        obtained = self.model._select(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        expected = ('SELECT id, key FROM table_name WHERE id=? and key=?', ('1', 'value'), 'strList', '|')
        self.assertEqual(expected, obtained)

    def test_should_get_many_fields_that_satisfy_the_condition(self):
        self.model.get(
            fields=('id', 'key')
            ,where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        self.model._run_sql_query.assert_called_with(
            operation='SELECT id, key FROM table_name WHERE id=? and key=?'
            ,parameters=('1', 'value')
            ,format='strList'
            ,separator='|'
            ,fetchAll=True)

    def test_should_get_all_fields_that_satisfy_the_condition(self):
        self.model.get(
            where='id=? and key=?'
            ,params=('1', 'value')
            ,format='strList'
            ,separator='|')
        self.model._run_sql_query.assert_called_with(
            operation='SELECT * FROM table_name WHERE id=? and key=?'
            ,parameters=('1', 'value')
            ,format='strList'
            ,separator='|'
            ,fetchAll=True)

    def test_should_get_the_table_with_an_specific_rowid(self):
        self.model.get(
            fields='rowid'
            ,where='rowid=?'
            ,params='1')
        self.model._run_sql_query.assert_called_with(
            operation='SELECT rowid FROM table_name WHERE rowid=?'
            ,parameters=('1',)
            ,format=None
            ,separator='|'
            ,fetchAll=True)

    def test_should_return_an_delete_query_with_one_parameter(self):
        obtained = self.model._delete(where='id=?', params='1')
        expected = ('DELETE FROM table_name WHERE id=?', ('1',))
        self.assertEqual(expected, obtained)

    def test_should_return_an_delete_query_with_many_parameters(self):
        obtained = self.model._delete(where='id=? and key=?', params=('1', 'value'))
        expected = ('DELETE FROM table_name WHERE id=? and key=?', ('1', 'value'))
        self.assertEqual(expected, obtained)

    def test_should_call_delete_and_run_sql_query(self):
        self.model.remove(where='id=?', params='1')
        self.model._run_sql_query.assert_called_with(
            operation='DELETE FROM table_name WHERE id=?'
            ,parameters=('1',)
            ,commit=True)

    def test_should_call_has_item_method(self):
        obtained = self.model._has_item(where='id=?', params='1')
        expected = ('SELECT * FROM table_name WHERE id=?', ('1',))
        self.assertEqual(expected, obtained)

    def testh_should_call_vacuum_method(self):
        self.model.vacuum()
        self.model._run_sql_query.assert_called_with(operation='VACUUM', commit=True)

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


class ModelServicesTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('sqlite3model.db', autocommit=False)
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

    def tearDown(self):
        os.remove('sqlite3model.db')

    def test_should_return_an_update_query(self):
        self.model._run_sql_query = Mock()
        obtained = self.model._update(
            fields={'numero': 444444444}
            ,where='id=?'
            ,params=1)
        expected = ('UPDATE model_name SET numero=? WHERE id=?', (444444444, 1))
        self.assertEqual(expected, obtained)

    def test_should_cal_set_an_update_query(self):
        self.model._run_sql_query = Mock()

        obtained = self.model.update(
            fields={'numero': 444444444}
            ,where='id=?'
            ,params=1)
        self.model._run_sql_query.assert_called_with(
            operation='UPDATE model_name SET numero=? WHERE id=?'
            ,parameters=(444444444, 1)
            ,commit=True)


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



class FormatResultsTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('sqlite3model.db', autocommit=False)
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
        os.remove('sqlite3model.db')

    def test_should_get_result_in_strList_format(self):
        obtained = self.model.get(format='strList')
        expected = ['1|111111111|primer texto', '2|222222222|segundo texto']
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_default_format(self):
        obtained = self.model.get(format='default')
        expected = [(1, 111111111, 'primer texto'), (2, 222222222, 'segundo texto')]
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_tupleList_format(self):
        obtained = self.model.get(format='tupleList')
        expected = [(1, 111111111, 'primer texto'), (2, 222222222, 'segundo texto')]
        self.assertEqual(expected, obtained)

    def test_should_get_result_in_dictList_format(self):
        obtained = self.model.get(format='dictList')
        expected = [{'texto': 'primer texto', 'id': 1, 'numero': 111111111}, {'texto': 'segundo texto', 'id': 2, 'numero': 222222222}]
        self.assertEqual(expected, obtained)


    def test_should_get_result_in_strList_format(self):
        data = self.model.get(format='object')[0]
        # self.assertIsInstance(data, sqlite3Model.NamedTuple)
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


class BooleanTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection(':memory:')
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


if __name__ == '__main__':
    unittest.main()