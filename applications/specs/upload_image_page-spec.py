import unittest
from unittest.mock import Mock
import test
from applications.newarticle.controllers import upload_image_page


class UploadImagePageComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.upload = upload_image_page.UploadImagePage(
            dependencies=test.mocks)
        self.upload.handler()

    def test_should_be_an_instance_of_UploadImagePage(self):
        self.assertIsInstance(self.upload, upload_image_page.UploadImagePage)

    def test_should_exist_template_file(self):
        self.assertFileExists(self.upload.loggedTemplate)

    def test_should_exist_unauthorized_template(self):
        self.assertFileExists(self.upload.unauthorizedTemplate)

    def test_should_show_the_form(self):
        self.upload.session.validate = Mock(return_value=True)
        self.upload.handler()
        expected = dict(
            context={
                'title': 'Subir Archivos'
                ,'salir': True}
            ,templatePath=self.upload.loggedTemplate)
        self.assertEqual(expected, self.upload._logged)

    def test_should_show_the_unauthorized(self):
        self.upload.session.validate = Mock(return_value=False)
        self.upload.handler()
        expected = dict(
            context={
                'title': 'Sin permiso'
                ,'salir': False}
            ,templatePath=self.upload.unauthorizedTemplate)
        self.assertEqual(expected, self.upload._unlogged)


if __name__ == '__main__':
    unittest.main()