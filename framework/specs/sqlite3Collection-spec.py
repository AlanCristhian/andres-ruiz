import os
import sys
import unittest
import sqlite3

from unittest.mock import Mock

oldDirectory = os.getcwd()
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from database import sqlite3Collection
os.chdir(oldDirectory)


class CollectionComponentTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('collection-test.db')
        # self.collection._run_sql_query = Mock()
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection._set_database_path = Mock()

    def tearDown(self):
        os.remove('collection-test.db')

    def test_should_call_set_database_path_and_return_self(self):
        expected = self.collection.path('anoter/path')
        self.collection._set_database_path.assert_called_with('anoter/path')
        self.assertEqual(self.collection, expected)

    def test_should_return_database_path(self):
        expected = self.collection.path()
        self.assertEqual('collection-test.db', expected)

    def test_should_call_create_model_and_run_sql_query(self):
        self.collection.create(name='test', fields={
            'byte_key': 'bytes',
            'integer_key': 'int',
            'primary_key': 'intPrim',
            'real_key': 'float',
            'string_key': 'str'})
        self.collection.connection.execute.assert_called_with('CREATE TABLE IF NOT EXISTS test (byte_key BLOB, integer_key INTEGER, primary_key INTEGER PRIMARY KEY, real_key REAL, string_key TEXT)')

    def test_should_make_an_create_table_sentence(self):
        obtained = self.collection._create_model(
            name ='test_table',
            fields = {
                'id': 'int'
                ,'key': 'str'})
        expected = 'CREATE TABLE IF NOT EXISTS test_table (id INTEGER, key TEXT)'
        self.assertEqual(obtained, expected)

    def test_should_make_an_create_table_sentence_with_primary_key(self):
        obtained = self.collection._create_model(
            name ='test_table',
            fields = {
                'id': 'prim'
                ,'key': 'str'})
        expected = 'CREATE TABLE IF NOT EXISTS test_table (id PRIMARY KEY, key TEXT)'
        self.assertEqual(obtained, expected)

    def test_should_make_an_delete_table_sentence(self):
        obtained = self.collection._remove_model(name ='test_table')
        expected = 'DROP TABLE IF EXISTS test_table'
        self.assertEqual(obtained, expected)

    def test_should_raise_an_error_for_an_ivalid_argument(self):
        self.assertRaises(TypeError, self.collection._create_model,
            name ='test_table',
            fields = {
                'id': 'int'
                ,'key': 'str'}
            ,error='an invalid key')

    def test_should_raise_an_error_for_an_invalid_table_name(self):
        self.assertRaises(TypeError, self.collection._remove_model, fields='test_table')

    def test_should_raise_an_error_for_an_Null_table_name(self):
        self.assertRaises(TypeError, self.collection._remove_model)

    def test_should_raise_an_error_for_fields_required(self):
        self.assertRaises(TypeError, self.collection._create_model, 'test_table')

    def test_should_be_raise_an_error_for_invalid_type_field(self):
        self.assertRaises(KeyError, self.collection._create_model,
            name ='test_table',
            fields = {
                'id': 'int'
                ,'key': 'invalidType'})

    def test_should_call_remove_model_and_run_sql_query(self):
        self.collection.remove('test')
        self.collection.connection.execute.assert_called_with('DROP TABLE IF EXISTS test')

    def test_should_convert_bool_to_BOOLEAN(self):
        obtained = self.collection._create_model(
            name='bool_test'
            ,fields={
                'id': 'prim'
                ,'boolean_key': 'bool'})
        expected = 'CREATE TABLE IF NOT EXISTS bool_test (boolean_key BOOLEAN, id PRIMARY KEY)'
        self.assertEqual(obtained, expected)


class CollectionServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.collection = sqlite3Collection.Collection('collection-has-test.db', autocommit=False)
        self.collection\
            .create(
                name='test',
                fields = {
                    'id': 'int'
                    ,'key': 'str'})

    def tearDown(self):
        os.remove('collection-has-test.db')

    def test_should_check_table_existence(self):
        doNotHasTable = self.collection.has('any_table')
        self.assertEqual(doNotHasTable, False)
        hasTable = self.collection.has('test')
        self.assertEqual(hasTable, True)

    def test_should_get_fields(self):
        obtained = self.collection._fields('test').sort()
        expected = ['id', 'key'].sort()
        self.assertEqual(obtained, expected)


class CollectionTriggersTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('trigger-test.db', autocommit=False)
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

    def tearDown(self):
        os.remove('trigger-test.db')

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


@unittest.skip('Not work yet')
class ForeingKeyTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('foreing-key-test.db', autocommit=False)
        self.collection.create(name='articles', fields={
            'id': 'intPrim'
            ,'title': 'str'
            ,'content': 'str'})

    def tearDown(self):
        os.remove('foreing-key-test.db')

    def test_should_find_an_invalid_type(self):
        self.assertRaises(KeyError, self.collection.set,
            name='not_valid_type_table', fields={
                'id': 'intPrim'
                ,'title': 'str'
                ,'content': 'str'
                ,'not_valid_type': 'not.valid'})

    def test_should_make_an_create_table_query(self):
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        obtained = self.collection.set(name='images', fields={
            'id': 'intPrim'
            ,'name': 'str'
            ,'fromarticle': 'articles.id'
        })
        expected = 'CREATE TABLE IF NOT EXISTS images(fromarticle NULL, id INTEGER PRIMARY KEY, name TEXT, FOREIGN KEY(fromarticle) REFERENCES articles(id) ON INSERT CASCADE ON DELETE CASCADE ON UPDATE CASCADE)'
        self.collection.connection.execute.assert_called_with(expected)


@unittest.skip('Not work yet')
class ForeignKeyIntegrityTest(unittest.TestCase):

    def setUp(self):
        # self.collection = sqlite3Collection.Collection('collection-integrity-test.db', autocommit=False)
        self.collection = sqlite3Collection.Collection(':memory:', autocommit=False)
        self.collection\
            .create(name='articles', fields={
                    'id': 'intPrim'
                    ,'description': 'str'
                    ,'article_name': 'str'})\
            .set(name='images', fields={
                    'id': 'intPrim'
                    ,'description': 'str'
                    ,'article_name': 'articles.article_name'})
        self.articles = self.collection.get('articles')
        self.images = self.collection.get('images')
        self.articles.insert(article_name='first_article', description='An article description')
        self.articles.insert(article_name='second_article', description='Another article description')
        self.images.insert(article_name='first_article', description='first image')
        self.images.insert(article_name='first_article', description='second image')
        self.images.insert(article_name='second_article', description='first image in second_article')
        self.images.insert(article_name='second_article', description='second image in second_article')

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


class TriggersIntegrityTest(unittest.TestCase):

    def setUp(self):
        # self.collection = sqlite3Collection.Collection('collection-integrity-test.db', autocommit=False)
        self.collection = sqlite3Collection.Collection(':memory:', autocommit=False)
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

    # def tearDown(self):
    #     os.remove('collection-integrity-test.db')

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


class BooleanTypeTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('boolean-test.db', autocommit=False)

    def tearDown(self):
        os.remove('boolean-test.db')

    def test_should_set_boolean_value(self):
        self.collection.create(
            name='bool_test'
            ,fields={
                'id':           'prim'
                ,'boolean_key': 'bool'})
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=True)

    def test_should_get_boolean_value_as_True(self):
        self.collection.create(
            name='bool_test'
            ,fields={
                'id':           'prim'
                ,'boolean_key': 'bool'})
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=True)
        obtained = self.boolModel.get(
            fields='boolean_key'
            ,format='dictList')[0]
        expected = {'boolean_key': True}
        self.assertEqual(expected, obtained)

    def test_should_get_boolean_value_as_False(self):
        self.collection.create(
            name='bool_test'
            ,fields={
                'id':           'prim'
                ,'boolean_key': 'bool'})
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=False)
        obtained = self.boolModel.get(
            fields='boolean_key'
            ,format='dictList')[0]
        expected = {'boolean_key': False}
        self.assertEqual(expected, obtained)

    def test_should_be_an_instance_of_boolean_class(self):
        self.collection.create(
            name='bool_test'
            ,fields={
                'id':           'prim'
                ,'boolean_key': 'bool'})
        self.boolModel = self.collection.get('bool_test')
        self.boolModel.insert(boolean_key=False)
        false_result = self.boolModel.get(
            fields='boolean_key'
            ,where='boolean_key=?'
            ,params=(False,)
            ,format='dictList')[0]
        self.assertIsInstance(false_result['boolean_key'], bool)


class TableModificationTest(unittest.TestCase):

    def setUp(self):
        self.collection = sqlite3Collection.Collection('modification-test.db', autocommit=False)
        self.collection.create(name='test_table', fields={
            'id': 'prim'
            ,'string': 'str'
            ,'boolean': 'bool'
            ,'integer': 'int'})
        self.table = self.collection.get('test_table')

    def tearDown(self):
        os.remove('modification-test.db')

    def test_should_make_a_query_that_add_one_field(self):
        obtained = self.collection._add_fields(name='table_name', fields={'real_key': 'float'})
        expected = 'ALTER TABLE table_name ADD COLUMN real_key REAL;'
        self.assertEqual(expected, obtained)

    def test_should_make_a_query_that_add_many_fields(self):
        obtained = self.collection._add_fields(name='table_name', fields={
            'real_key': 'float'
            ,'str_key': 'str'})
        expected = \
"""ALTER TABLE table_name ADD COLUMN real_key REAL;
ALTER TABLE table_name ADD COLUMN str_key TEXT;"""
        self.assertEqual(expected, obtained)

    def test_should_call_add_fields_method(self):
        self.collection._add_fields = Mock()
        self.collection.connection = Mock()
        self.collection.connection.execute = Mock()
        self.collection.add_fields('table_name', {'real_key': 'float'})
        self.collection._add_fields.assert_called_with('table_name', {'real_key': 'float'})

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
        obtained = self.collection._remove_fields(name='my_table', fields='c')
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
        self.assertEqual(expected, obtained)


    def test_should_make_a_query_that_remove_many_fields(self):
        self.collection.create('my_table', {'a': 'int', 'b': 'str', 'c': 'float', 'd': 'bool'})
        obtained = self.collection._remove_fields(name='my_table', fields=('c', 'd'))
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
        self.assertEqual(expected, obtained)

    def test_should_remove_any_fields(self):
        self.collection.remove_fields('test_table', ('boolean', 'integer'))
        obtained = self.collection._fields('test_table').sort()
        expected = ['id', 'string'].sort()
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()