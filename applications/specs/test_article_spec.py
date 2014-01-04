import unittest
from unittest.mock import Mock, call
import test
from applications.home.controllers import article


class ArticleSpec(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.article = article.Article(dependencies=test.mocks)

    def test_Article_instance(self):
        """Should make an instance of article.Article.
        """
        self.assertIsInstance(self.article, article.Article)

    def test_template_existence(self):
        """The template file should exists.
        """
        self.article.handler()
        self.assertFileExists(self.article.loggedTemplatePath)

    def test_article_property(self):
        """should has the article property.
        """
        self.article.clientModel.get.assert_called_with('articles')
        self.assertHasAttr(self.article, 'articles')

    def test_shared_ssl_url(self):
        """Should remove the username and "images" to the shared ssl.
        """
        self.article.config.enableSharedSSL = True
        self.article.clientModel.url = '/~andresru/proyectos/article'
        self.article.clientModel.https = 'YES'

        self.article.handler()

        obtained = self.article.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    def test_non_ssl_url(self):
        """Should remove "images" form the url.
        """
        self.article.enableSharedSSL = True
        self.article.clientModel.url = '/proyectos/article'
        self.article.clientModel.https = False

        self.article.handler()

        obtained = self.article.article_URL
        expected = 'article'
        self.assertEqual(obtained, expected)

    @unittest.skip('not work the test case')
    def test_article_property(self):
        """Shoud store an instance of an article binded to current url.
        """
        self.article.serverCollection.get = Mock()
        self.article.articles.get = Mock(return_value=[{'title': 'Article'}])
        self.article.handler()
        self.assertCalled(self.article.articles.get)

    @unittest.skip('not work the test case')
    def test_invalid_article_url(self):
        """Shoud show the 404 error.
        """
        self.article.articles.get = Mock(return_value=[])
        self.article.basic_response = Mock()
        self.article.clientModel.url = '/~andresru/proyectos/article'

        self.article.handler()
        self.article.basic_response.assert_called_with(
            templatePath='applications/error/error404.html',
            context={
                'url': self.article.clientModel.url,
                'title': '404 No encontrado',
                'salir': False
            },
            status=404
        )

    @unittest.skip('not work the test case')
    def test_valid_article_url(self):
        """Should show the article.
        """

        self.article.get = Mock(return_value=[{'title': 'Article'}])
        self.article.clientModel.url = '/~andresru/proyectos/article'
        self.article.basic_response = Mock()

        self.article.handler()
        self.article.basic_response.assert_called_with(
            templatePath=self.article.loggedTemplatePath,
            context={
                'url': self.article.clientModel.url,
                'title': 'Article',
                'salir': False
            },
            status=404

        )


if __name__ == '__main__':
    unittest.main()