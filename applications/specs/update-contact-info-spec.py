import unittest
from unittest.mock import Mock
import test
from applications.editContact.controllers import update_contact_info


class InfoComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.info = update_contact_info.UpdateInfo(dependencies=test.mocks)
        self.info.clientModel.form = {
            'id': 1
            ,'usser_name': 'alan_cristhian'
            ,'address': 'example 123'
            ,'email': 'example@domain.com'
            ,'facebook': 'facebook.com/alan.cristh'
            ,'twitter': 'twitter.com/AlanCristh'
            ,'pinterest': 'pinterest.com/alancristhian'
            ,'telephone': '12345'
            ,'mobile': '67890'}
        self.info.handler()

    def test_should_have_an_contact_info_instance(self):
        self.assertIsInstance(self.info, update_contact_info.UpdateInfo)

    def test_should_get_contact_model(self):
        self.info.serverCollection.get.assert_called_with('contact')

    def test_should_save_client_info(self):
        self.info.contact.update.assert_called_with(
            fields={
                'address': 'example 123'
                ,'email': 'example@domain.com'
                ,'facebook': 'facebook.com/alan.cristh'
                ,'twitter': 'twitter.com/AlanCristh'
                ,'pinterest': 'pinterest.com/alancristhian'
                ,'telephone': '12345'
                ,'mobile': '67890'}
            ,where='id=?'
            ,params='1')

    def test_should_send_void_response(self):
        self.info.basic_response=Mock()
        self.info.handler()
        self.info.basic_response.assert_called_with(
            content={'status': 'ok'}
            ,contentType='application/json'
            ,status=204)


if __name__ == '__main__':
    unittest.main()