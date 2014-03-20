import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import remove_multimedia


class RemoveMultimediaTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.removeMultimedia = remove_multimedia.RemoveMultimedia(dependencies=test.mocks)
        self.removeMultimedia.clientModel.form = {
            'id': 1
            ,'url': '8a7sdfa8s7fd.jpg'
        }
        self.removeMultimedia.setUp()
        self.removeMultimedia.remove = Mock()

    def test_removeMultimedia_instance(self):
        """Should has an instance of RemoveMultimedia class."""
        self.assertIsInstance(self.removeMultimedia, remove_multimedia.RemoveMultimedia)

    def tests_logged_response(self):
        """Should response an json object with an status message."""
        self.removeMultimedia.logged_response = Mock()
        self.removeMultimedia.handler();
        self.removeMultimedia.logged_response.assert_called_with(
            content={'status': 'The multimedia whas removed.'}
        )

    def test_remove_multimedia_of_database(self):
        """Should remove the multimedia of the database."""
        self.removeMultimedia.multimedia.remove = Mock()
        self.removeMultimedia.handler()
        self.removeMultimedia.multimedia.remove.assert_called_with(
            where='id=?', params=1)

    def test_folder_removal(self):
        """Should clear the multimedia of the database."""
        self.removeMultimedia.multimedia.get = Mock(return_value=['any/path'])
        self.removeMultimedia.handler()
        self.removeMultimedia.remove.assert_called_with('8a7sdfa8s7fd.jpg')


if __name__ == '__main__':
    unittest.main()