import unittest
from unittest.mock import Mock
import test
from applications.home.controllers import get_article_images as get_images


class GetArticleImplementation(unittest.TestCase, test.CustomAssertions):
    """Test the spec of GetArticleModel.
    """
    def setUp(self):
        self.get_images = get_images.GetArticleModel(dependencies=test.mocks)

    def test_shared_ssl_url(self):
        """Should remove the username and "images" to the shared ssl.
        """
        self.get_images.config.enableSharedSSL = True
        self.get_images.clientModel.url = '/~andresru/images/article'
        self.get_images.clientModel.https = 'YES'

        self.get_images.setUp()

        obtained = self.get_images.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    def test_non_ssl_url(self):
        """Should remove "images" form the url.
        """

        self.get_images.enableSharedSSL = True
        self.get_images.clientModel.url = '/images/article'
        self.get_images.clientModel.https = False

        self.get_images.setUp()

        obtained = self.get_images.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    def test_article_property(self):
        """Should has the image attribute.
        """
        self.get_images.setUp()
        self.assertHasAttr(self.get_images, 'article')

    def test_images_property(self):
        """Should has the image attribute.
        """
        self.get_images.setUp()
        self.assertHasAttr(self.get_images, 'images')


class GetArticleSpec(unittest.TestCase, test.CustomAssertions):
    """Test the spec of GetArticleModel.
    """
    def setUp(self):
        self.get_images = get_images.GetArticleModel(dependencies=test.mocks)

    def test_serverCollection_get_article(self):
        """Should get the article table.
        """
        self.get_images.setUp()
        self.get_images.serverCollection.get.assert_any_call('articles')

    def test_GetArticleModel_instance(self):
        """Should make an instance of GetArticleModel.
        """
        self.assertIsInstance(self.get_images, get_images.GetArticleModel)

    def test_get_article_name(self):
        """Should has the get_article_name() method.
        """
        self.assertHasAttr(self.get_images, "get_article_name")

    def test_get_images(self):
        """Should has get_images() method.
        """
        self.assertHasAttr(self.get_images, 'get_images')

    def test_non_valid_article_url(self):
        """Should show an error message if the article url is not valid.
        """
        self.get_images.setUp()
        self.get_images.get_article_name = Mock(return_value=[])
        self.get_images.basic_response = Mock()
        self.get_images.article_URL = 'article'

        self.get_images.handler()
        self.get_images.basic_response.assert_called_with(
            content={'error': 'article not exists'},
            contentType='application/json',
        )

    def test_call_get_image(self):
        """Should call get_image() if the article URL is valid.
        """
        self.get_images.setUp()
        self.get_images.get_article_name = Mock(
            return_value=[('article_name',)])
        self.get_images.get_images = Mock()

        self.get_images.handler()
        self.get_images.get_images.assert_called_with('article_name')

    def test_image_data_response(self):
        """Should response a list with image data."""
        self.get_images.setUp()
        self.get_images.get_article_name = Mock(
            return_value=[('article_name',)])
        self.get_images.get_images = Mock(
            return_value=[
                {'url': 'image/1', 'description': 'description 1'},
                {'url': 'image/2', 'description': 'description 2'},
        ])
        self.get_images.basic_response = Mock()

        self.get_images.handler()
        self.get_images.basic_response.assert_called_with(
            content=[
                {'url': 'image/1', 'description': 'description 1'},
                {'url': 'image/2', 'description': 'description 2'},
            ],
            contentType='application/json',
        )


if __name__ == '__main__':
    unittest.main()