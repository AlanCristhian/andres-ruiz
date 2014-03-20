import unittest
import test
from unittest.mock import Mock
from applications.editArticle.controllers import save_multimedia_data


class BaseTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_multimedia_data.SaveMultimediaData(dependencies=test.mocks)

    def test_content_type(self):
        """The content type of response must be 'application/json'."""
        self.saveData.setUp()
        self.saveData.response.set_content_type.assert_called_with(
            'application/json')

    def test_SaveMultimediaData_instance(self):
        """Should has an instance of SaveMultimediaData class."""
        self.assertIsInstance(self.saveData, save_multimedia_data.SaveMultimediaData)


class NewMultimediaTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_multimedia_data.SaveMultimediaData(
            dependencies=test.mocks, warnings=False)
        self.saveData.clientModel.form = {
            'url': ''
            ,'description': ''
            ,'article_name': 'test-article-name-1'
            ,'cid': 'c8'
        }
        self.saveData.setUp()

    def test_multimedia_creation(self):
        """Should call the create_new_multimedia()
        method if the form has the id key.
        """
        self.saveData.clientModel.form = {}
        self.saveData.create_new_multimedia = Mock()
        self.saveData.handler()
        self.assertCalled(self.saveData.create_new_multimedia)

    def test_first_data_inserted(self):
        """Should set the creation date after the creation."""
        self.saveData.clientModel.form = {}
        self.saveData.create_new_multimedia()
        self.assertCalled(self.saveData.multimedia.update)


    def test_get_the_current_multimedia(self):
        """Should get the current"""
        self.saveData.multimedia.lastModelIdChanged = 1
        self.saveData.multimedia.get = Mock(return_value=[{}])
        self.saveData.handler()
        self.saveData.multimedia.get.assert_called_with(
            fields=('id', 'article_name', 'description', 'url', 'cover')
            ,where='id=?'
            ,params=1
            ,format='dictList'
        )

    def test_new_multimedia_response(self):
        """Should send a response with the new multimedia data."""
        self.saveData.multimedia.get = Mock(return_value=[{
            'id': 1
            ,'article_name': 'test-article-name-1'
            ,'description': ''
            ,'url': ''
        }])
        self.saveData.handler()
        self.saveData.basic_response(
            content={
                'id': 1
                ,'article_name': 'test-article-name-1'
                ,'description': ''
                ,'url': ''  
            }
        )


class ExistentMultimediaTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_multimedia_data.SaveMultimediaData(dependencies=test.mocks)
        self.saveData.clientModel.form = {
            'id': 1
            ,'url': ''
            ,'description': 'The description of the content.'
        }
        self.saveData.setUp()
        self.saveData.multimedia.get = Mock(return_value=[None])

    def test_multimedia_updating(self):
        """Should call the update_multimedia_data()
        method if the form haven't the id key.
        """
        self.saveData.update_multimedia_data = Mock()
        self.saveData.handler()
        self.assertCalled(self.saveData.update_multimedia_data)

    def test_multimedia_fields_updating(self):
        """Should update the fields in the database."""
        self.saveData.update_multimedia_data()
        self.saveData.multimedia.update.assert_called_with(
            fields= {
                'description': 'The description of the content.'
                ,'url': ''
                ,'last_modified': self.saveData.date
            }
            ,where='id=?'
            ,params=1
        )

    @unittest.expectedFailure
    def test_cover_update(self):
        """Should set the first multimedia of the article as the cover multimedia.
        """
        raise AssertionError

    @unittest.expectedFailure
    def test_cover_update_if_delete(self):
        """Should change the cover multimedia if is deleted the first multimedia.
        """
        raise AssertionError


if __name__ == '__main__':
    unittest.main()