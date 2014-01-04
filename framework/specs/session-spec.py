import unittest
from unittest.mock import Mock
import test
from framework import session


class SessionComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.session = session.Session(
            servermodelDependence=test.mocks.serverCollection
            ,configDependence=test.mocks.config
            ,clientModelDependence=test.mocks.clientModel
        )

    def test_should_be_an_instance_of_Session(self):
        self.assertIsInstance(self.session, session.Session)

    def test_should_create_a_session_collection(self):
        self.assertTrue(self.session.servermodel.create.called)

    def test_should_remove_expires_sessions(self):
        self.assertTrue(self.session.model.remove.called)

    @unittest.skip('deprecated')
    def test_should_get_client_id(self):
        self.assertTrue(self.session.clientModel.get_cookie.called)

    def test_should_be_a_visitor_if_no_cookies(self):
        self.assertFalse(self.session.validate())

    def tests_should_be_a_visitor_if_clientID_no_in_sessions(self):
        self.session.clientID = 'abc123'
        self.session.model.get = Mock(return_value=[])
        self.assertFalse(self.session.validate())

    def test_should_be_a_user_if_found_clientID_in_sessions(self):
        self.session.clientID = 'abc123'
        self.data = {
            'id': 'abc123'
            ,'data': 'any data'
            ,'created_time': '1'
            ,'accessed_time': '2'
            ,'expire_time': '3'
            ,'remote_addr': '4'
        }
        self.session.model.get = Mock(return_value=[self.data])
        self.assertTrue(self.session.validate())

    def test_should_equal_serverID_and_clientID(self):
        self.session.clientID = 'abc123'
        self.data = {
            'id': 'abc123'
            ,'data': 'any data'
            ,'created_time': '1'
            ,'accessed_time': '2'
            ,'expire_time': '3'
            ,'remote_addr': '4'
        }
        self.session.model.get = Mock(return_value=[self.data])
        self.session.validate()
        self.assertEqual(self.session.clientID, self.session.serverID)

    def test_should_get_all_session_data(self):
        self.session.clientID = 'abc123'
        self.data = {
            'id': 'abc123'
            ,'data': 'any data'
            ,'created_time': '1'
            ,'accessed_time': '2'
            ,'expire_time': '3'
            ,'remote_addr': '4'
        }
        self.session.model.get = Mock(return_value=[self.data])
        # self.session._get_session_data = Mock(return_value=self.data)
        self.session.validate()
        self.assertHasAttr(self.session, 'data')

    @unittest.skip('deprecated')
    def test_should_update_session_data(self):
        self.session.clientID = 'abc123'
        self.data = {
            'id': 'abc123'
            ,'data': 'any data'
            ,'created_time': '1'
            ,'accessed_time': '2'
            ,'expire_time': '3'
            ,'remote_addr': '4'
        }
        self.session.model.get = Mock(return_value=[self.data])
        self.session.validate()
        self.assertTrue(self.session.model.update.called)

    def test_should_create_a_new_session_id(self):
        self.session.model.get = Mock(return_value=[])
        self.id = self.session._create_new_id()
        self.assertTrue(self.id)

    def test_should_create_a_new_session(self):
        self.session.model.get = Mock(return_value=[])
        self.session.create()
        self.assertHasAttr(self.session, 'newSessionId')

    def test_should_remove_sessions(self):
        self.session.remove()
        self.session.model.remove.assert_called_with(
            where="id=?"
            ,params=None)


if __name__ == '__main__':
    unittest.main()