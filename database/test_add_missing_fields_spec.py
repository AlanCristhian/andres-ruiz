import unittest
from unittest.mock import Mock

from framework import test
from . import add_missing_fields

from framework import servermodel


class TestContactInfoTable(unittest.TestCase, test.CustomAssertions):
    """Test for the new contact_info table."""
    def setUp(self):
        self.missing_data = add_missing_fields.AddMissingData()
        self.missing_data.collection.create = Mock()
        self.missing_data.collection.insert = Mock()
        self.missing_data.collection.get = Mock()
        self.missing_data.collection.bind = Mock()
        self.missing_data.add_contact_info_table()

    def test_missing_data_instance(self):
        self.assertIsInstance(self.missing_data,
            add_missing_fields.AddMissingData)

    def test_collection_attribute(self):
        self.assertIsInstance(self.missing_data.collection,
            servermodel.Collection)

    def test_contact_info_table(self):
        self.missing_data.collection.create.assert_called_with(
            name='contact_info',
            fields={
                'id':               'prim',
                'service_name':     'str',
                'service_address':  'str',
                'user_name':        'str',
                'data':             'str',
            },
        )

    def test_contact_info_bindig(self):
        self.missing_data.collection.bind.assert_called_with(
            bindName='contact_info_to_users',
            modelSource='contact_info',
            fieldSource='user_name',
            modelTarget='users',
            fieldTarget='user_name',
        )

    def test_contact_info_attribute(self):
        """Should create the contact_info attribute."""
        self.assertHasAttr(self.missing_data, 'contact_info')

    def test_contact_attribute(self):
        """Should create the contact attribute."""
        self.assertHasAttr(self.missing_data, 'contact')

    @unittest.skip('need implement the test')
    def test_contact_info_fields_insertion(self):
        """"""

class TestMultimediaTable(unittest.TestCase, test.CustomAssertions):
    """Test for the new multimedia table."""
    def setUp(self):
        self.multimedia = add_missing_fields.AddMissingData()
        self.multimedia.collection.create = Mock()
        self.multimedia.collection.insert = Mock()
        self.multimedia.collection.get = Mock()
        self.multimedia.collection.bind = Mock()

    def test_multimedia_table(self):
        self.multimedia.add_multimedia_table()
        self.multimedia.collection.create.assert_called_with(
            name='multimedia',
            fields={
                'id':              'intPrim',
                'creation_date':   'datetime',
                'last_modified':   'datetime',
                'url':             'str',
                'description':     'str',
                'classification':  'str',
                'article_name':    'str',
                'position':        'int',
                'acceptance':      'float',
                'zoomed':          'int',
                'likes':           'int',
                'dislikes':        'int',
                'data':            'str',
                'cover':           'bool',
                'type':            'str',
            }
        )

    def test_multimedia_binding(self):
        self.multimedia.add_multimedia_table()
        self.multimedia.collection.bind.assert_called_with(
            bindName='multimedia_to_articles',
            modelSource='multimedia',
            fieldSource='article_name',
            modelTarget='articles',
            fieldTarget='article_name'
        )

    @unittest.skip('need be implemented')
    def test_multimedia_fill(self):
        """"""


class TestAddMissingData(unittest.TestCase, test.CustomAssertions):
    """Test for the new contact_info table."""
    def setUp(self):
        self.missing_data = add_missing_fields.AddMissingData()
        self.missing_data.collection.add_fields = Mock()
        self.missing_data.add_missing_fields()

    def test_articles_data_field(self):
        """Should add the *data* field to the *articles* table."""
        self.missing_data.collection.add_fields.assert_any_call(
            name='articles', fields={'data': 'str'})

    def test_comments_data_field(self):
        """Should add the *data* field to the *comments* table."""
        self.missing_data.collection.add_fields.assert_any_call(
            name='comments', fields={'data': 'str'})

    def test_visitors_data_field(self):
        """Should add the *data* field to the *visitors* table."""
        self.missing_data.collection.add_fields.assert_any_call(
            name='visitors', fields={'data': 'str'})

    def test_users_data_field(self):
        """Should add the *data* field to the *users* table."""
        self.missing_data.collection.add_fields.assert_any_call(
            name='users', fields={'data': 'str'})


class TestRemoveTables(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.missing_data = add_missing_fields.AddMissingData()
        self.missing_data.collection.remove = Mock()
        self.missing_data.remove_tables()

    def test_deletion_of_images_table(self):
        self.missing_data.collection.remove.assert_any_call(name='images')

    def test_deletion_of_videos_table(self):
        self.missing_data.collection.remove.assert_any_call(name='videos')

    def test_deletion_of_location_table(self):
        self.missing_data.collection.remove.assert_any_call(name='location')

    @unittest.skip('not used')
    def test_deletion_of_contact_table(self):
        self.missing_data.collection.remove.assert_any_call(name='contact')


if __name__ == '__main__':
    unittest.main()