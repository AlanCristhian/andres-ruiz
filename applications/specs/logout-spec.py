import unittest
from unittest.mock import Mock
import test
from applications.logout.controllers import logout


class LogoutComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.logout = logout.Logout(dependencies=test.mocks)
        self.logout.handler()

    def test_should_is_instance_of_logout(self):
        self.assertIsInstance(self.logout, logout.Logout)

    def test_should_exists_themplate(self):
        self.assertFileExists(self.logout.templatePath)

    def test_should_remove_session_from_server(self):
        self.assertCalled(self.logout.session.remove)


if __name__ == '__main__':
    unittest.main()