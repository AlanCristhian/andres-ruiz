import http.cookies
import json
import os
import itertools
import types

from framework import helpers
from framework import security


class Model:
    """Manages the information received by the client"""

    def __init__(self):
        """Puth the os.environ dict into the namespace"""
        self.__dict__.update(
            itertools.starmap(
                lambda key, value: (
                    key[0].lower() +  # upper case the first letter and add
                    key.title()       # title case all text
                    .replace('_', '') # remove undersore
                    [1:]              # all text without the first char
                , value
                ) #lambda
                ,os.environ.items()
            ) #itertools.starmap
        ) #update

    @property
    def form(self):
        """Contains the data send from the client."""
        return security.get_field_storage()

    @property
    def cookie(self):
        """The client cookie"""
        return http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))

    @property
    def url(self):
        """The url of request"""
        url = os.environ.get('PATH_INFO')\
            or os.environ.get('REQUEST_URI')
        return url if url else ''

    @property
    def serverProtocol(self):
        """The server protocol"""
        serverProtocol = os.environ.get('SERVER_PROTOCOL')
        return serverProtocol if serverProtocol else 'HTTP/1.1'

    @property
    def protocol(self):
        """Te protocol (HTTP or HTTPS)"""
        return helpers.get_protocol()

    @property
    def ip(self):
        """The ip of the client"""
        return os.environ.get('REMOTE_ADDR')
        