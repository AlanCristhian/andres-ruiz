"""This library manages HTTP responses"""

import http.cookies
import datetime
import json
import os
from codecs import decode

from framework import config
from framework import helpers

class Response:
    """Manage the HTTP response"""
    def __init__(self, settings=config.Config):
        self.config = settings()
        self.statusTemplate = {
            '101': '101 Switching Protocols',
            '200': '200 OK',
            '201': '201 Created',
            '202': '202 Accepted',
            '203': '203 Non-Authoritative Information',
            '204': '204 No Content',
            '205': '205 Reset Content',
            '206': '206 Partial Content',
            '300': '300 Multiple Choices',
            '301': '301 Moved Permanently',
            '302': '302 Found',
            '303': '303 See Other',
            '304': '304 Not Modified',
            '305': '305 Use Proxy',
            '307': '307 Temporary Redirect',
            '400': '400 Bad Request',
            '401': '401 Unauthorized',
            '402': '402 Payment Required',
            '403': '403 Forbidden',
            '404': '404 Not Found',
            '405': '405 Method Not Allowed',
            '406': '406 Not Acceptable',
            '407': '407 Proxy Authentication Required',
            '408': '408 Request Time-out',
            '409': '409 Conflict',
            '410': '410 Gone',
            '411': '411 Length Required',
            '412': '412 Precondition Failed',
            '413': '413 Request Entity Too Large',
            '414': '414 Request-URI Too Large',
            '415': '415 Unsupported Media Type',
            '416': '416 Requested range not satisfiable',
            '417': '417 Expectation Failed',
            '500': '500 Internal Server Error',
            '501': '501 Not Implemented',
            '502': '502 Bad Gateway',
            '503': '503 Service Unavailable',
            '504': '504 Gateway Time-out',
            '505': '505 HTTP Version not supported'
        }
        self.contentTypeTemplate = {
            'text/html': 'Content-Type: text/html'
            ,'text/plain': 'Content-Type: text/plain'
            ,'application/json': 'Content-Type: application/json'
            # ,'': 'Content-Type: '
        }
        self.charsetTemplate = {
            'utf-8': 'charset=utf-8'
            # ,'': 'charset='
        }
        self.responseTemplate = "{self.protocol}"\
                                "{self.status}\r"\
                                "{self.date}"\
                                "{self.location}"\
                                "{self.expires}"\
                                "{self.server}"\
                                "{self.contentType}; "\
                                "{self.charset}"\
                                "{self.contentLenght}"\
                                "{self.cookie}"\
                                "{self.endHeader}"\
                                "{self.body}"

        # default properties
        self.endHeader = os.linesep
        self.body = ''
        self.settings = settings
        self._set_protocol()
        self._set_server()
        self._set_date()

        # user defined properties
        self.set_status()
        self.set_content_type()
        self.set_charset()
        self.set_expires()
        self.redirect()
        self.set_cookie()

    def render(self, body):
        """Fill the fields on template."""
        if 'application/json' in self.contentType:
            self.body = json.dumps(body)
        else:
            self.body = body
        self._set_content_lenght(self.body)
        result = self.responseTemplate.format(self=self)
        return result

    def set(self, function, *args, **kwargs):
        setters = {
            'status': self.set_status
            ,'contentType': self.set_content_type
            ,'charset': self.set_charset
            ,'expires': self.set_expires
            ,'redirect': self.redirect
            ,'cookie': self.set_cookie
        }
        setters[function](*args, **kwargs)

    def set_status(self, status='200'):
        """Set status field."""
        self.status = self.statusTemplate[str(status)]

    def set_content_type(self, contentType='text/html'):
        """Set Content-Type field"""
        self.contentTypeShortcut = contentType
        self.contentType = self.contentTypeTemplate[contentType]

    def set_charset(self, charset='utf-8'):
        """Set charset field"""
        self.charset = self.charsetTemplate[charset] + os.linesep
        self.encoding = charset

    def set_expires(self, expires=0):
        """Set Expires field."""
        expires = expires or self.config.expirationDate
        self.expires = 'Expires: ' + self._set_GMDDate(expires) + os.linesep

    def redirect(self, location=''):
        """Set location field"""
        protocol = helpers.get_protocol()
        if location:
            if self.config.serverName in location:
                self.location = 'Location: ' + protocol + '://' \
                              + location + os.linesep
            else:
                if self.config.enableSharedSSL:
                    self.location = 'Location: ' + protocol + '://' \
                                  + self.config.sharedSSLPath \
                                  + location + os.linesep  
                else:
                    self.location = 'Location: ' + protocol + '://' \
                                  + self.config.serverName \
                                  + location + os.linesep          
        else:
            self.location = ''

    def set_cookie(self, name=None, value=None, max_age=None,
        path='/', domain=None, secure=False, httponly=False):
        """Set a cooke field in response."""
        name = name or self.config.cookieName
        if value:
            cookie = http.cookies.SimpleCookie()
            cookie[name] = value
            cookie[name]['path'] = path
            if max_age:
                cookie[name]['max-age'] = max_age
            if domain:
                cookie[name]['domain'] = domain
            if secure:
                cookie[name]['secure'] = secure
            if httponly:
                cookie[name]['httponly'] = httponly
            self.cookie = str(cookie)
        else:
            self.cookie = ''

    def get_content_type(self):
        return self.contentTypeShortcut

    # Private methods

    def _set_protocol(self):
        """Set server Protocol field."""
        self.protocol = os.environ.get('SERVER_PROTOCOL') or 'HTTP/1.1 '

    def _set_server(self):
        """Set server field."""
        self.server = 'Server: {server}{linesep}'\
            .format(
                server=os.environ.get('SERVER_SOFTWARE') or 'terminal'
                ,linesep=os.linesep
            )

    def _set_date(self):
        """Set date field."""
        self.date = 'Date: ' + self._set_GMDDate(0) + os.linesep

    def _set_content_lenght(self, body):
        """Set Content-Length field."""
        if isinstance(body, str):
            bodyLength = len(body)
        else:
            bodyLength = len(repr(body))
        self.contentLenght = 'Content-Length: ' + repr(bodyLength) + os.linesep

    def _set_GMDDate(self, days=0):
        """Return a date with GMT format."""
        date = datetime.datetime.now() + datetime.timedelta(days)
        return date.strftime('%a, %d %b %Y %H:%M:%S GMT')