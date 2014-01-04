import unittest
import test
from unittest.mock import Mock
from applications.editArticle.controllers import save_image_data


class BaseTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_image_data.SaveImageData(dependencies=test.mocks)

    def test_content_type(self):
        """The content type of response must be 'application/json'."""
        self.saveData.setUp()
        self.saveData.response.set_content_type.assert_called_with(
            'application/json')

    def test_SaveImageData_instance(self):
        """Should has an instance of SaveImageData class."""
        self.assertIsInstance(self.saveData, save_image_data.SaveImageData)


class NewImageTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_image_data.SaveImageData(dependencies=test.mocks)
        self.saveData.clientModel.form = {
            'url': ''
            ,'description': ''
            ,'article_name': 'test-article-name-1'
            ,'cid': 'c8'
        }
        self.saveData.setUp()

    def test_image_creation(self):
        """Should call the create_new_image()
        method if the form has the id key.
        """
        self.saveData.clientModel.form = {}
        self.saveData.create_new_image = Mock()
        self.saveData.handler()
        self.assertCalled(self.saveData.create_new_image)

    def test_first_data_inserted(self):
        """Should set the creation date after the creation."""
        self.saveData.clientModel.form = {}
        self.saveData.create_new_image()
        self.assertCalled(self.saveData.images.update)


    def test_get_the_current_image(self):
        """Should get the current"""
        self.saveData.images.lastModelIdChanged = 1
        self.saveData.images.get = Mock(return_value=[{}])
        self.saveData.handler()
        self.saveData.images.get.assert_called_with(
            fields=('id', 'article_name', 'description', 'url')
            ,where='id=?'
            ,params=1
            ,format='dictList'
        )

    def test_new_image_response(self):
        """Should send a response with the new image data."""
        self.saveData.images.get = Mock(return_value=[{
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


class ExistentImageTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_image_data.SaveImageData(dependencies=test.mocks)
        self.saveData.clientModel.form = {
            'id': 1
            ,'url': ''
            ,'description': 'The description of the content.'
        }
        self.saveData.setUp()
        self.saveData.images.get = Mock(return_value=[None])

    def test_image_updating(self):
        """Should call the update_image_data()
        method if the form haven't the id key.
        """
        self.saveData.update_image_data = Mock()
        self.saveData.handler()
        self.assertCalled(self.saveData.update_image_data)

    def test_image_fields_updating(self):
        """Should update the fields in the database."""
        self.saveData.update_image_data()
        self.saveData.images.update.assert_called_with(
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
        """Should set the first image of the article as the cover image.
        """
        raise AssertionError

    @unittest.expectedFailure
    def test_cover_update_if_delete(self):
        """Should change the cover image if is deleted the first image.
        """
        raise AssertionError


if __name__ == '__main__':
    unittest.main()