import unittest
from unittest.mock import Mock
import test
from applications.login.controllers import login


class LoginComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.login = login.Login(dependencies=test.mocks)
        self.login.handler()

    def test_should_be_an_Login_instance(self):
        self.assertIsInstance(self.login, login.Login)

    def test_should_exists_template(self):
        self.assertFileExists(self.login.loginTemplate)

    def test_should_redirect_to_admin_home(self):
        self.login.warnings = False
        self.login.clientModel.form = {}
        self.login.redirect_to_admin_home = Mock()
        self.login.handler()
        self.assertCalled(self.login.redirect_to_admin_home)

    def test_should_get_users_model(self):
        self.login.warnings = False
        self.login.clientModel.form = {
            'user': 'alan'
            ,'password': '123'}
        self.login.get_user_data = Mock(return_value=[{
            'user_name': 'alan'
            ,'password': '123'}])
        self.login.handler()
        self.assertCalled(self.login.get_user_data)

    def test_should_get_invalid_user_name(self):
        self.login.warnings = False
        self.login.clientModel.form = {
            'user': 'alan'
            ,'password': '123'}
        self.login.get_user_data = Mock(return_value=[])
        self.login.handler()
        self.assertEqual(self.login._unlogged['context']['userLabel'], 'No existe ese usuario')

    def test_should_get_invalid_password(self):
        self.login.warnings = False
        self.login.clientModel.form = {
            'user': 'alan'
            ,'password': '123'}
        self.login.get_user_data = Mock(return_value=[{'password': 'abc'}])
        self.login.handler()
        self.assertEqual(self.login._unlogged['context']['passLabel'], 'Contraseña no válida')
    
    def test_should_redirect_to_admin_home_and_create_new_sesssion(self):
        self.login.warnings = False
        self.login.clientModel.form = {
            'user': 'alan'
            ,'password': '123'}
        self.login.get_user_data = Mock(return_value=[{'password': '123'}])
        self.login.create_new_session = Mock()
        self.login.handler()
        self.assertCalled(self.login.create_new_session)


if __name__ == '__main__':
    unittest.main()