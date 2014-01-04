import test
import unittest
from unittest.mock import Mock
from applications.shared.controllers import check_ssl_environ


class CheckSSLEnvironTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.check = check_ssl_environ.CheckSSLEnviron(dependencies=test.mocks)
        self.check.config.enableSharedSSL = Mock()
        self.check.basic_response = Mock()

    def test_should_exist_an_instance(self):
        self.assertIsInstance(self.check, check_ssl_environ.CheckSSLEnviron)

    def test_should_return_that_is_not_shared_ssl(self):
        self.check.config.enableSharedSSL = False
        self.check.handler()
        self.check.basic_response.assert_called_with(
            content='False'
            ,contentType='text/plain')

    def test_should_return_that_is_shared_ssl(self):
        self.check.config.enableSharedSSL = True
        self.check.handler()
        self.check.basic_response.assert_called_with(
            content='True'
            ,contentType='text/plain')


if __name__ == '__main__':
    unittest.main()