import unittest
import test
from unittest.mock import Mock
from applications.editArticle.controllers import save_article_data


class SaveArticleComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.saveData = save_article_data.SaveData(dependencies=test.mocks)

    def test_should_has_an_instance_of_SaveData(self):
        self.assertIsInstance(self.saveData, save_article_data.SaveData)


if __name__ == '__main__':
    unittest.main()