import unittest
from unittest.mock import Mock
import test
from applications.newarticle.controllers import validate_field


class ValidateComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.validate = validate_field.Validate(dependencies=test.mocks)

    def test_should_be_an_instance_of_Validate(self):
        self.assertIsInstance(self.validate, validate_field.Validate)

    def test_should_exists_article_name(self):
        self.validate.clientModel.form = {'article_name': 'Article Name'}
        self.validate.get_articles_model = Mock(return_value={
            'article_name': [('article-name',)]})
        self.validate.handler()
        self.assertEqual(self.validate._basic, {'content': {'exists': True}})

    def test_should_not_exists_article_name(self):
        self.validate.clientModel.form = {'article_name': 'Article Name'}
        self.validate.get_articles_model = Mock(return_value={
            'article_name': []})
        self.validate.handler()
        self.assertEqual(self.validate._basic, {'content': {'exists': False}})


if __name__ == '__main__':
    unittest.main()