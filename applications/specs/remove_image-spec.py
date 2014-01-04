import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import remove_image


class RemoveImageTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.removeImage = remove_image.RemoveImage(dependencies=test.mocks)
        self.removeImage.clientModel.form = {
            'id': 1
            ,'url': '8a7sdfa8s7fd.jpg'
        }
        self.removeImage.setUp()
        self.removeImage.remove = Mock()

    def test_removeImage_instance(self):
        """Should has an instance of RemoveImage class."""
        self.assertIsInstance(self.removeImage, remove_image.RemoveImage)

    def tests_logged_response(self):
        """Should response an json object with an status message."""
        self.removeImage.logged_response = Mock()
        self.removeImage.handler();
        self.removeImage.logged_response.assert_called_with(
            content={'status': 'The image whas removed.'}
        )

    def test_remove_image_of_database(self):
        """Should remove the image of the database."""
        self.removeImage.images.remove = Mock()
        self.removeImage.handler()
        self.removeImage.images.remove.assert_called_with(
            where='id=?', params=1)

    def test_folder_removal(self):
        """Should clear the image of the database."""
        self.removeImage.images.get = Mock(return_value=['any/path'])
        self.removeImage.handler()
        self.removeImage.remove.assert_called_with('8a7sdfa8s7fd.jpg')


if __name__ == '__main__':
    unittest.main()