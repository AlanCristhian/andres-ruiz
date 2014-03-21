import test
import unittest
from unittest.mock import Mock
from applications.newarticle.controllers import create_new_article


class NewArticleComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.new = create_new_article.NewArticle(dependencies=test.mocks)
        self.new.logged = Mock()
        self.new.clientModel.form = {'article_name': 'Any Name'}

    def test_should_has_an_NewArticle_instance(self):
        self.assertIsInstance(self.new, create_new_article.NewArticle)

    def test_should_be_an_existing_article_name(self):
        self.new.get_article_name = Mock(return_value=[('any-name',)])
        self.new.handler()
        self.new.logged.assert_called_with(content={'exists': True})

    def test_should_be_create_the_new_article(self):
        self.new.get_article_name = Mock(return_value=[])
        self.new.create_article = Mock(return_value=True)
        self.new.handler()
        self.new.logged.assert_called_with(
            content={'status': True, 'edit_url': 'admin/editar/any-name'})

    def test_should_be_not_create_the_article(self):
        self.new.get_article_name = Mock(return_value=[])
        self.new.create_article = Mock(return_value=False)
        self.new.handler()
        self.new.logged.assert_called_with(content={'status': False})

    def test_should_insert_an_new_article_row(self):
        self.new.handler()
        self.new.articles.insert.assert_called_with(
            article_name='any-name'
            ,title='Any Name'
            ,url='any-name'
            ,edit_url='admin/editar/any-name'
            ,creation_date=self.new.date
            ,last_modified=self.new.date
            ,directory=':memory:/files/any-name-folder')

    def test_should_create_the_folder_path(self):
        self.new.handler()
        obtained = self.new.articlePath
        expected = ':memory:/files/any-name-folder'
        self.assertEqual(obtained, expected)

    def test_should_create_the_article_directorie(self):
        self.new.handler()
        self.new.mkdir.assert_called_with(':memory:/files/any-name-folder')


if __name__ == '__main__':
    unittest.main()