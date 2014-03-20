import unittest
from unittest.mock import Mock
import test

from applications.editArticle.controllers import get_list_of_articles
from framework import security


class EditArticleComponents(unittest.TestCase, test.CustomAssertions):
    
    def setUp(self):
        self.article_list = get_list_of_articles.ListOfArticles(
            dependencies=test.mocks)
        self.article_list.setUp()

    def test_instance_of_EditArticle(self):
        """Should has an instance of EditArticle."""
        self.assertIsInstance(self.article_list,
            get_list_of_articles.ListOfArticles)

    def test_articles_property(self):
        """Should has the .articles property."""
        self.assertHasAttr(self.article_list, 'articles')

    def test_article_list_property(self):
        """Should has the .article_list property."""
        self.assertHasAttr(self.article_list, 'article_list')

    def test_get_first_paragraph_method(self):
        """Should return the first paragraph of an text."""
        obtained = self.article_list.get_first_paragraph('a\nb')
        expected = 'a'
        self.assertEqual(obtained, expected)

    def test_update_fields_method(self):
        """Should have the .update_fields() method."""
        self.assertHasAttr(self.article_list, 'update_fields')


if __name__ == '__main__':
    unittest.main()
