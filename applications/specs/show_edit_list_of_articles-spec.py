import unittest
from unittest.mock import Mock
import test
from applications.editArticle.controllers import show_edit_list_of_articles


class EditArticleComponents(unittest.TestCase, test.CustomAssertions):
    
    def setUp(self):
        self.edit = show_edit_list_of_articles.EditArticle(dependencies=test.mocks)
        self.edit.handler()

    def test_should_to_be_an_instance_of_EditArticle(self):
        self.assertIsInstance(self.edit, show_edit_list_of_articles.EditArticle)

    def test_should_exists_template_path(self):
        self.assertFileExists(self.edit.templatePath)



if __name__ == '__main__':
    unittest.main()