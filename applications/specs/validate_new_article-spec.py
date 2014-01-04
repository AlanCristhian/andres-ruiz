import unittest
from unittest.mock import Mock
import test
from applications.newarticle.controllers import validate_new_article


class ValidateArticleComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.validate = validate_new_article.ValidateArticle()
        self.validate.warnings = False
        self.validate.clientModel.get_form = Mock(return_value={'have-data': True})

    def test_should_be_an_instance_of_ValidateArticle(self):
        self.validate.handler()
        self.assertIsInstance(self.validate, validate_new_article.ValidateArticle)

    def test_should_exists_ok_template(self):
        self.validate.handler()
        self.assertFileExists(self.validate.sendOkTemplate)

    def test_should_exists_unauthorized_template(self):
        self.validate.handler()
        self.assertFileExists(self.validate.unauthorizedTemplate)

    def test_should_create_unlogged_response(self):
        self.validate.unlogged = Mock()
        self.validate.handler()
        self.validate.unlogged.assert_called_with(
            context={
                'title': 'Sin permiso'
                ,'salir': False}
            ,templatePath=self.validate.unauthorizedTemplate)

    def test_should_get_form_data(self):
        self.validate.clientModel.get_form = Mock()
        self.validate.handler()
        self.assertCalled(self.validate.clientModel.get_form)

    def test_should_not_have_data(self):
        self.validate.clientModel.get_form = Mock(return_value={})
        self.validate.logged = Mock()
        self.validate.handler()
        self.validate.logged.assert_called_with(
            context={
                'title': 'Debe rellenar los campos correctamente'
                ,'salir': True}
            ,templatePath=self.validate.sendOkTemplate)

    def test_should_have_data(self):
        self.validate.clientModel.get_form = Mock(return_value={'have-data': True})
        self.validate.create = Mock()
        self.validate.handler()
        self.assertCalled(self.validate.create)

    def test_should_create_article(self):
        self.validate.create = Mock(return_value=True)
        self.validate.logged = Mock()
        self.validate.handler()
        self.validate.logged.assert_called_with(
            context={
                'title': 'Los datos han sido enviados con éxtio'
                ,'salir': True}
            ,templatePath=self.validate.sendOkTemplate)

    def test_should_do_not_create_article(self):
        self.validate.create = Mock(return_value=False)
        self.validate.logged = Mock()
        self.validate.handler()
        self.validate.logged.assert_called_with(
            context={
                'title': 'Ha ocurrido un error durante la creación del documento. Por favor Póngase en contacto con Alan Cristhian.'
                ,'salir': True}
            ,templatePath=self.validate.sendOkTemplate)

    def test_should_get_ARTICLES_model(self):
        self.validate.serverCollection.get = Mock()
        self.validate.handler()
        self.assertHasAttr(self.validate, 'articles')

    def test_should_get_IMAGES_model(self):
        self.validate.serverCollection.get = Mock()
        self.validate.handler()
        self.assertHasAttr(self.validate, 'images')

    def test_should_get_VIDEOS_model(self):
        self.validate.serverCollection.get = Mock()
        self.validate.handler()
        self.assertHasAttr(self.validate, 'videos')

    def test_should_set_creation_date(self):
        self.validate.helpers.get_datetime = Mock(return_value='now')
        self.validate.handler()
        self.assertEqual(self.validate.creationDate, 'now')

    def test_should_set_project_name(self):
        self.validate.clientModel.get_form = Mock(return_value={
            'project_name': 'Project Name'})
        self.validate.handler()
        self.assertEqual(self.validate.projectName, 'project-name')

if __name__ == '__main__':
    unittest.main()