import unittest
from unittest.mock import Mock
import test
from applications.newarticle.controllers import show_new_article_form


class NewArticleFormComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.newArticleForm = show_new_article_form.NewArticleForm()
        self.newArticleForm.handler()

    def test_should_exists_template_path(self):
        self.assertFileExists(self.newArticleForm.loggedTemplatePath)
        self.assertFileExists(self.newArticleForm.unloggedTemplatePath)

    def test_should_show_new_article_form(self):
        obtained = self.newArticleForm._logged
        expected = {
            'context': {
                'title': 'Crear Nuevo Artículo'
                ,'salir': True}
            ,'templatePath': self.newArticleForm.loggedTemplatePath}
        self.assertEqual(obtained, expected)

    def test_should_show_unauthorized_page(self):
        obtained = self.newArticleForm._unlogged
        expected = {
            'context': {
                'title': 'Sin permiso'
                ,'salir': False}
            ,'templatePath': self.newArticleForm.unloggedTemplatePath
            ,'status': 401}
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()