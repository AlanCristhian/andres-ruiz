import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import remove_article


class RemoveArticleTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.removeArticle = remove_article.RemoveArticle(dependencies=test.mocks)
        self.removeArticle.clientModel.form = {
            'id': 1
            ,'title': 'Test Article Name'
        }
        self.removeArticle.setUp()
        self.removeArticle.rmtree = Mock()

    def test_RemoveArticle_instance(self):
        """Should has an instance of RemoveArticle class."""
        self.assertIsInstance(self.removeArticle, remove_article.RemoveArticle)

    def tests_logged_response(self):
        """Should response an json object with the status key and the article
        title in the value.
        """
        self.removeArticle.logged_response = Mock()
        self.removeArticle.handler();
        self.removeArticle.logged_response.assert_called_with(
            content={'status': 'The article Test Article Name whas removed.'}
        )

    def test_remove_article_of_database(self):
        """Should remove the article of the database."""
        self.removeArticle.articles.remove = Mock()
        self.removeArticle.handler()
        self.removeArticle.articles.remove.assert_called_with(
            where='id=?', params=1)

    def test_folder_removal(self):
        """Should clear the folder of the article."""
        self.removeArticle.articles.get = Mock(return_value=['any/path'])
        self.removeArticle.handler()
        self.removeArticle.rmtree.assert_called_with('any/path')


if __name__ == '__main__':
    unittest.main()