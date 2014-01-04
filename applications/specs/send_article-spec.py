import unittest
from unittest.mock import Mock
import test
from applications.articles.controllers import send_article as send


class SendComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.send = send.Main(dependencies=test.mocks)
        self.list = [
            {}
            ,{}
        ]
        self.send.serverCollection.serverModel.get = Mock(return_value=self.list)
        self.send.handler()

    def test_should_to_be_an_instance_of_Main(self):
        self.assertIsInstance(self.send, send.Main)

    def test_should_get_articles_models(self):
        self.send.get_articles()
        self.send.serverCollection.get\
            .assert_called_with('articles')

    def test_should_get_images_models(self):
        self.send.get_images()
        self.send.serverCollection.get\
            .assert_called_with('images')

    @unittest.skip('not found')
    def test_should_get_a_list_of_articles(self):
        self.assertEqual(self.send.articlesList, {})

    def test_should_exists_template_path(self):
        self.assertFileExists(self.send.loggedTemplatePath)

    def test_should_has_404_status(self):
        self.send.serverCollection.serverModel.get = Mock(return_value=[])
        self.send.handler()
        self.send.response.set_status.assert_called_with(404)

    def test_should_exists_404_template(self):
        self.send.serverCollection.serverModel.get = Mock(return_value=[])
        self.send.handler()
        self.assertFileExists(self.send.loggedTemplatePath)


if __name__ == '__main__':
    unittest.main()