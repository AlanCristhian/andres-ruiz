import unittest
from unittest.mock import Mock, call
import test
from applications.home.controllers import get_article_collection


class ArticleCollectionImplementation(unittest.TestCase,
        test.CustomAssertions):
    """Test the implementation of the module.
    """
    def setUp(self):
        self.article_collection = get_article_collection.ArticleCollection(
            dependencies=test.mocks, warnings=False)
        self.article_collection.setUp()

    def test_get_data_instance(self):
        """Should creat an instance of the 'articles' table and the 'multimedia'
        table.
        """
        _calls = [call('articles'), call('multimedia')]
        self.article_collection.serverCollection.get.assert_has_calls(_calls)

    def test_get_article_list(self):
        self.article_collection.articles.get.assert_called_with(
            fields=('id', 'title', 'article_name', 'url', 'description'),
            format='dictList',
        )

    def test_get_first_paragraph(self):
        expected = 'abc'
        obtained = self.article_collection.get_first_paragraph('abc\ndefg')
        self.assertEqual(expected, obtained)



class ArticleCollectionSpec(unittest.TestCase, test.CustomAssertions):
    """Test for the module that send an array of objects.
    """
    def setUp(self):
        self.article_collection = get_article_collection.ArticleCollection(
            dependencies=test.mocks)

    def test_ArticleCollection_instance(self):
        """Would be able to create an instance of ArticleCollection class.
        """
        self.assertIsInstance(self.article_collection,
            get_article_collection.ArticleCollection)

    def test_basic_response(self):
        self.article_collection.basic_response = Mock()
        self.article_collection.handler()
        self.article_collection.basic_response.asert_called_with(
            content=[{'one': 1}, {'two': 2}],
            contentType='application/json',
        )


if __name__ == '__main__':
    unittest.main()