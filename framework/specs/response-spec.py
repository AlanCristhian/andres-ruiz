import os
import sys
import unittest
import sqlite3

from unittest.mock import Mock

oldDirectory = os.getcwd()
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from framework import response
# os.chdir(oldDirectory)


class ResponseComponents(unittest.TestCase):
    def setUp(self):
        self.resp = response.Response()

    def test_should_return_a_basic_response(self):
        self.resp.set_expires(7)
        expected = "HTTP/1.1 200 OK\r"\
            + 'Date: ' + self.resp._set_GMDDate() + '\n' \
            + 'Expires: ' + self.resp._set_GMDDate(7) + '\n' \
            + 'Server: terminal\n'\
            + 'Content-Type: text/html; '\
            + 'charset=utf-8\n'\
            + 'Content-Length: 4' + '\n' \
            + '\n'\
            + 'test'
        obtained = self.resp.render('test')
        self.assertEqual(expected, obtained)

    def test_should_set_protocol(self):
        expected = 'HTTP/1.1 '
        self.resp._set_protocol()
        self.assertEqual(expected, self.resp.protocol)

    def test_should_set_status(self):
        self.resp.set_status('404')
        expected = '404 Not Found'
        self.assertEqual(expected, self.resp.status)

    def test_should_set_date(self):
        self.resp._set_date()
        expected = 'Date: ' + self.resp._set_GMDDate() + '\n'
        self.assertEqual(expected, self.resp.date)

    def test_should_set_location(self):
        self.resp.redirect('localhost/page')
        expected = 'Location: http://localhost/page\n'
        self.assertEqual(expected, self.resp.location)

    def test_should_set_location_if_not_server_name(self):
        self.resp.config = Mock()
        self.resp.config.enableSharedSSL = False
        self.resp.config.serverName = 'localhost'
        self.resp.redirect('/page')
        expected = 'Location: http://localhost/page\n'
        self.assertEqual(expected, self.resp.location)

    def test_should_set_shared_ssl_location_if_not_server_name(self):
        self.resp.config = Mock()
        self.resp.config.enableSharedSSL = True
        self.resp.config.sharedSSLPath = 'shared.ssl/~path'
        self.resp.config.serverName = 'localhost'
        self.resp.redirect('/page')
        expected = 'Location: http://shared.ssl/~path/page\n'
        self.assertEqual(expected, self.resp.location)

    def test_should_set_expires(self):
        self.resp.set_expires(7)
        expected = 'Expires: ' + self.resp._set_GMDDate(7) + '\n'
        self.assertEqual(expected, self.resp.expires)

    def test_should_set_server(self):
        self.resp._set_server()
        expected = 'Server: terminal\n'
        self.assertEqual(expected, self.resp.server)

    def test_should_set_content_type(self):
        self.resp.set_content_type('text/plain')
        expected = 'Content-Type: text/plain'
        self.assertEqual(expected, self.resp.contentType)

    def test_should_set_charset(self):
        self.resp.set_charset('utf-8')
        expected = 'charset=utf-8\n'
        self.assertEqual(expected, self.resp.charset)

    def test_should_set_content_lenght(self):
        self.resp._set_content_lenght('12345')
        expected = 'Content-Length: 5\n'
        self.assertEqual(expected, self.resp.contentLenght)

    def test_should_return_content_type(self):
        self.resp.set_content_type('text/plain')
        obtained = self.resp.get_content_type()
        expected = 'text/plain'
        self.assertEqual(expected, obtained)

    def test_should_execute_all_methods(self):
        self.resp.set_status = Mock()
        self.resp.set_content_type = Mock()
        self.resp.set_charset = Mock()
        self.resp.set_expires = Mock()
        self.resp.redirect = Mock()
        self.resp.set_cookie = Mock()
        
        self.resp.set('status', '200')
        self.resp.set_status.assert_called_with('200')
        self.resp.set('contentType', 'text/plain')
        self.resp.set_content_type.assert_called_with('text/plain')
        self.resp.set('charset', 'utf-8')
        self.resp.set_charset.assert_called_with('utf-8')
        self.resp.set('expires', '1')
        self.resp.set_expires.assert_called_with('1')
        self.resp.set('redirect', 'any http address')
        self.resp.redirect.assert_called_with('any http address')
        self.resp.set('cookie', 'any cookie')
        self.resp.set_cookie.assert_called_with('any cookie')

    def test_should_raise_key_error(self):
        self.assertRaises(KeyError, self.resp.set, 'not valid key', '200')


if __name__ == '__main__':
    unittest.main()