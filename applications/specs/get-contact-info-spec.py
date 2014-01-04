import unittest
from unittest.mock import Mock
import test
from applications.editContact.controllers import get_contact_info


class ContactInfoComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.contactInfo = get_contact_info.ContactInfo(dependencies=test.mocks)
        self.contactInfo.handler()

    def test_should_be_an_ContactInfo_instance(self):
        self.assertIsInstance(self.contactInfo, get_contact_info.ContactInfo)

    def test_should_get_contact_model(self):
        self.assertCalled(self.contactInfo.serverCollection.get)

    def test_should_get_contact_info(self):
        self.assertCalled(self.contactInfo.contact.get)

    def test_should_send_response_with_data(self):
        self.contactInfo.warnings = False
        self.model = Mock()
        self.model.get = Mock(return_value=[{'any key': 'any value'}])
        self.contactInfo.serverCollection.get = Mock(return_value=self.model)
        self.contactInfo.basic_response = Mock()
        self.contactInfo.handler()
        self.contactInfo.basic_response.assert_called_with(
            content={'any key': 'any value'}
            ,contentType='application/json')

    def test_should_send_void_response(self):
        self.contactInfo.warnings = False
        self.model = Mock()
        self.model.get = Mock(return_value=[])
        self.contactInfo.serverCollection.get = Mock(return_value=self.model)
        self.contactInfo.basic_response = Mock()
        self.contactInfo.handler()
        self.contactInfo.basic_response.assert_called_with(
            content={}
            ,contentType='application/json')



if __name__ == '__main__':
    unittest.main()