import unittest
from unittest.mock import Mock
import test
from applications.editContact.controllers import contact


class ContactComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.contact = contact.Contact(dependencies=test.mocks)
        self.contact.handler()

    def test_should_has_instance_of_Contact(self):
        self.assertIsInstance(self.contact, contact.Contact)

    def test_should_exists_template(self):
        self.assertFileExists(self.contact.templatePath)

    def test_should_exists_unauthorized_template(self):
        self.assertFileExists(self.contact.unauthorized)

    def test_salir_should_be_true_if_logged(self):
        self.contact.session.validate = Mock(return_value=True)
        self.contact.handler()
        expected = dict(
            context=dict(
                title='Información de contacto'
                ,salir=True)
            ,templatePath=self.contact.templatePath)
        obtained = self.contact._logged
        self.assertEqual(obtained, expected)

    def test_salir_should_be_false_if_unlogged(self):
        self.contact.session.validate = Mock(return_value=False)
        self.contact.handler()
        expected = {
            'context': {
                'title': 'Sin permiso'
                ,'salir': False}
            ,'templatePath': self.contact.unauthorized}
        obtained = self.contact._unlogged
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()