import unittest
from unittest.mock import Mock
import test
from framework import router


class RouterComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.router = router.Router(settings=Mock())
        self.router.userHandlers = [
            {'/first_path': 'first_handler', '/second_path': 'second_handler'}
            ,{'/third_path': 'third_handler', '/fourth_path': 'fourth_handler'}]
        self.router.settings.sharedSSLPath = 'shared.ssl/~path'

    @unittest.skip('deprecated')
    def test_should_get_REQUEST_URI(self):
        self.router.environ = {
            'PATH_INFO': None
            ,'REQUEST_URI': '/request/uri'}
        expected = '/request/uri'
        obtained = self.router.get_path()
        self.assertEqual(expected, obtained)

    @unittest.skip('deprecated')
    def test_should_get_PATH_INFO(self):
        self.router.environ = {
            'PATH_INFO': '/path/info'
            ,'REQUEST_URI': None}
        expected = '/path/info'
        obtained = self.router.get_path()
        self.assertEqual(expected, obtained)

    def test_should_import_a_simple_module(self):
        module, function = self.router.import_module('fakeLibrary')
        expected = 'this is a function'
        obtained = module.function()
        self.assertEqual(expected, obtained)

    def test_should_import_a_DEFAULT_function_from_the_module(self):
        module, specific_function = self.router.import_module('fakeLibrary')
        expected = 'this is an default function'
        obtained = getattr(module, specific_function)()
        self.assertEqual(expected, obtained)

    def test_should_import_a_CUSTOM_function_from_the_module(self):
        module, custom_function = \
            self.router.import_module(('fakeLibrary', 'custom'))
        expected = 'this is an custom function'
        obtained = getattr(module, custom_function)()
        self.assertEqual(expected, obtained)


class RouterBehavior(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.router = router.Router(settings=Mock())
        self.router.userHandlers = [{
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'}]
        self.router.settings.sharedSSLPath = 'shared.ssl/~path'
        self.router.settings.sharedSSLDomain = 'shared.ssl'
        self.router.settings.enableSharedSSL = False
        self.router.environ = {
            'REQUEST_URI': '/any/request'
            ,'HTTPS': None
            ,'SERVER_NAME': 'server.name'
        }
        self.module = Mock()
        self.module.function = Mock()
        self.router.import_module = Mock(return_value=(self.module, 'function'))

    def test_should_set_a_know_simple_rute(self):
        self.router.route()
        expectedHandlers = {
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'}
        expected = '/any/request', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_unknow_simple_rute(self):
        self.router.environ['REQUEST_URI'] = 'unknow/request'
        self.router.route()
        expectedHandlers = {
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'}
        expected = '/error404', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_know_secure_route(self):
        self.router.environ['HTTPS'] = 'yes'
        self.router.route()
        expectedHandlers = {
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'}
        expected = '/any/request', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_unknow_secure_route(self):
        self.router.environ['REQUEST_URI'] = 'unknow/request'
        self.router.environ['HTTPS'] = 'yes'
        self.router.route()
        expectedHandlers = {
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'}
        expected = '/error404', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)



class SharedSSLTest(unittest.TestCase, test.CustomAssertions):
    """Test the shared ssl routing. Here use the following
    nomenclature:
    http://     example.com     /~user_name   /any/path
       |            |               |            |
    protocol    server name      user name      path
    """
    def setUp(self):
        self.router = router.Router(settings=Mock())
        self.router.userHandlers = [{
            '/any/request': 'handler'
            ,'/error404': 'errorHandler'
            ,'/existent/route': 'existent_handler'}]
        self.router.settings.sharedSSLPath = 'shared.ssl/~path'
        self.router.settings.sharedSSLDomain = 'shared.ssl'
        self.router.settings.sharedSSLUser = '/~path'
        self.router.settings.enableSharedSSL = False
        self.router.environ = {
            'REQUEST_URI': '/any/request'
            ,'HTTPS': None
            ,'SERVER_NAME': 'server.name'
        }
        self.module = Mock()
        self.module.function = Mock()
        self.router.import_module = Mock(return_value=(self.module, 'function'))

    def test_shared_ssl_user_name_in_all_handlers(self):
        """Should seth the user name of the shared ssl protocol in all key
        of each handler.
        """
        self.router.environ['HTTPS'] = 'yes'
        self.router.settings.enableSharedSSL = True
        self.router.route()
        expected = {
            '/~path/any/request': 'handler'
            ,'/~path/error404': 'errorHandler'
            ,'/~path/existent/route': 'existent_handler'}
        obtained = self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_know_secure_route_in_shared_ssl(self):
        self.router.environ['HTTPS'] = 'yes'
        self.router.environ['REQUEST_URI'] = '/~path/any/request'
        self.router.settings.enableSharedSSL = True
        self.router.route()
        expectedHandlers = {
            '/~path/any/request': 'handler'
            ,'/~path/error404': 'errorHandler'
            ,'/~path/existent/route': 'existent_handler'
        }
        expected = '/~path/any/request', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_unknow_secure_route_in_shared_ssl(self):
        self.router.environ['REQUEST_URI'] = '/unknow/request'
        self.router.environ['HTTPS'] = 'yes'
        self.router.settings.enableSharedSSL = True
        self.router.route()
        expectedHandlers = {
            '/~path/any/request': 'handler'
            ,'/~path/error404': 'errorHandler'
            ,'/~path/existent/route': 'existent_handler'}
        expected = '/~path/error404', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_should_set_a_void_secure_route_in_shared_ssl(self):
        self.router.environ['REQUEST_URI'] = '/unknow/request'
        self.router.environ['HTTPS'] = 'yes'
        self.router.settings.enableSharedSSL = True
        self.router.route()
        expectedHandlers = {
            '/~path/any/request': 'handler'
            ,'/~path/error404': 'errorHandler'
            ,'/~path/existent/route': 'existent_handler'}
        expected = '/~path/error404', expectedHandlers
        obtained = self.router.path, self.router.handler
        self.assertEqual(expected, obtained)

    def test_check_shared_ssl_path_existence(self):
        """Should exists the shared route in the handler list.
        """
        self.router.environ['REQUEST_URI'] = '/existent/route'
        self.router.environ['HTTPS'] = 'yes'
        self.router.settings.enableSharedSSL = True

        self.router.route()

        expected = '/~path/existent/route'
        obtained = self.router.path
        self.assertEqual(expected, obtained)



if __name__ == '__main__':
    unittest.main()