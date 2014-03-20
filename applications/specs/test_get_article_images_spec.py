import unittest
from unittest.mock import Mock
import test
import os
from applications.home.controllers import get_article_images as get_multimedia


os.environ.update({'REQUEST_URI': '/images/article'})


class GetArticleImplementation(unittest.TestCase, test.CustomAssertions):
    """Test the spec of GetArticleModel.
    """
    def setUp(self):
        self.get_multimedia = get_multimedia.GetArticleModel(dependencies=test.mocks)

    def test_shared_ssl_url(self):
        """Should remove the username and "images" to the shared ssl.
        """
        self.get_multimedia.config.enableSharedSSL = True
        self.get_multimedia.clientModel.url = '/~andresru/images/article'
        self.get_multimedia.clientModel.https = 'YES'

        self.get_multimedia.setUp()

        obtained = self.get_multimedia.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    def test_non_ssl_url(self):
        """Should remove "images" form the url.
        """

        self.get_multimedia.enableSharedSSL = True
        self.get_multimedia.clientModel.url = '/images/article'
        self.get_multimedia.clientModel.https = False

        self.get_multimedia.setUp()

        obtained = self.get_multimedia.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    def test_articles_property(self):
        """Should has the image attribute.
        """
        self.get_multimedia.setUp()
        self.assertHasAttr(self.get_multimedia, 'articles')

    def test_multimedia_property(self):
        """Should has the image attribute.
        """
        self.get_multimedia.setUp()
        self.assertHasAttr(self.get_multimedia, 'multimedia')


class GetArticleSpec(unittest.TestCase, test.CustomAssertions):
    """Test the spec of GetArticleModel.
    """
    def setUp(self):
        self.get_multimedia = get_multimedia.GetArticleModel(dependencies=test.mocks)

    def test_serverCollection_get_article(self):
        """Should get the article table.
        """
        self.get_multimedia.setUp()
        self.get_multimedia.serverCollection.get.assert_any_call('articles')

    def test_GetArticleModel_instance(self):
        """Should make an instance of GetArticleModel.
        """
        self.assertIsInstance(self.get_multimedia, get_multimedia.GetArticleModel)

    def test_get_multimedia(self):
        """Should has get_multimedia() method.
        """
        self.assertHasAttr(self.get_multimedia, 'get_multimedia')

    def test_non_valid_article_url(self):
        """Should show an error message if the article url is not valid.
        """
        self.get_multimedia.setUp()
        self.get_multimedia.article_name = []
        self.get_multimedia.basic_response = Mock()
        self.get_multimedia.article_URL = 'article'

        self.get_multimedia.handler()
        self.get_multimedia.basic_response.assert_called_with(
            content={'error': 'article not exists'},
            contentType='application/json',
        )

    @unittest.expectedFailure
    def test_call_get_image(self):
        """Should call get_image() if the article URL is valid.
        """
        self.get_multimedia.setUp()
        self.get_multimedia.article_name = [('article_name',)]
        self.get_multimedia.get_multimedia = Mock()

        self.get_multimedia.handler()
        self.get_multimedia.get_multimedia.assert_called_with()

    @unittest.expectedFailure
    def test_image_data_response(self):
        """Should response a list with image data."""
        self.get_multimedia.setUp()
        self.get_multimedia.article_name = [('article_name',)]
        self.get_multimedia.get_multimedia = Mock(
            return_value=[
                {'url': 'image/1', 'description': 'description 1'},
                {'url': 'image/2', 'description': 'description 2'},
        ])
        self.get_multimedia.basic_response = Mock()

        self.get_multimedia.handler()
        self.get_multimedia.basic_response.assert_called_with(
            content=[
                {'url': 'image/1', 'description': 'description 1'},
                {'url': 'image/2', 'description': 'description 2'},
            ],
            contentType='application/json',
        )


if __name__ == '__main__':
    unittest.main()