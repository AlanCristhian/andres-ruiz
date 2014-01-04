import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import edit_article


class EditArticleComponents(unittest.TestCase, test.CustomAssertions):
    
    def setUp(self):
        self.edit = edit_article.EditArticle(dependencies=test.mocks)
        self.edit.clientModel.url = '/any/url'

    def test_should_to_be_an_instance_of_EditArticle(self):
        self.edit.handler()
        self.assertIsInstance(self.edit, edit_article.EditArticle)

    def test_should_exists_template_path(self):
        self.edit.handler()
        self.assertFileExists(self.edit.templatePath)

    def test_should_get_article_data(self):
        self.edit.get_data = Mock(return_value={})
        self.edit.handler()
        self.assertCalled(self.edit.get_data)


if __name__ == '__main__':
    unittest.main()