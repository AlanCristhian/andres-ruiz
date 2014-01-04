import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import get_list_of_articles


class EditArticleComponents(unittest.TestCase, test.CustomAssertions):
    
    def setUp(self):
        self.listArticles = get_list_of_articles.ListOfArticles(
            dependencies=test.mocks)
        self.listArticles.setUp()

    def test_instance_of_EditArticle(self):
        """Should has an instance of EditArticle."""
        self.assertIsInstance(self.listArticles,
            get_list_of_articles.ListOfArticles)


if __name__ == '__main__':
    unittest.main()
