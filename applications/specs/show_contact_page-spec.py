import unittest
import test
from applications.contact.controllers import show_contact_page as contact


class ContactComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.contact = contact.Main(dependencies=test.mocks)
        self.contact.handler()

    def test_should_has_an_Main_instance(self):
        self.assertIsInstance(self.contact, contact.Main)

    def test_should_get_contact_info(self):
        self.contact.serverCollection.get.assert_called_with('contact')

    def test_should_exists_template_path(self):
        self.assertFileExists(self.contact.templatePath)

    def test_should_to_be_false_to_unlogged(self):
        self.assertEqual(self.contact.unloggedContext['salir'], False)

    def test_should_to_be_True_to_logged(self):
        self.assertEqual(self.contact.loggedContext['salir'], True)


if __name__ == '__main__':
    unittest.main()