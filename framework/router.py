import collections
import importlib
import os
import re


from framework import core


class Router:
    """docstring for Router"""

    def __init__(self, userHandlers=None, settings=None):
        # userHandlers is a module with many dictionaries
        self.userHandlers = [
            getattr(userHandlers, var)\
            for var in dir(userHandlers)\
            if not '__' in var
        ]
        self.settings = settings
        self.environ = os.environ

    def import_module(self, key):
        """Imports the module associated with key. The dictionary within
        systemHandlers can hold values ​​of type String, Tuple or List.
        """
        if isinstance(key, str):
            return (importlib.import_module(key), 'handler')
        if isinstance(key, tuple) or isinstance(key, list):
            module, function = key
            return (importlib.import_module(module), function)

    def route(self):
        """Get an dictionary with an regular expresssion key. Its
        value is a reference to a self.handler function.
        """
        # get the url of user browser
        self.path = (self.environ.get('PATH_INFO')\
                    or self.environ.get('REQUEST_URI')).replace('launch.py?q=', '')

        errorPath = '/error404'

        # set a dictionary which is a combination of all dictionaries
        self.handler = collections.ChainMap(*self.userHandlers)

        if self.environ.get('HTTPS'):
            # complete the url
            if self.settings.enableSharedSSL:
                # Fill the error path
                errorPath = self.settings.sharedSSLUser + errorPath
                systemHandlers = {}
                # Fill each key with the user name of the shared ssl protocol
                for key in self.handler:
                    systemHandlers.update({
                        self.settings.sharedSSLUser + key: self.handler[key]
                    })
                # fill the path of the request
                if self.settings.sharedSSLUser not in self.path:
                    self.path = self.settings.sharedSSLUser + self.path
                self.handler = systemHandlers

        # import the module with the request handler
        if self.path:
            if self.path not in self.handler:
                # chec the regular expressions
                result = self._find_re_handler(self.path)
                self.path = result or errorPath
        else:
            self.path = errorPath

        # get the custom handler if exists

        module, function = self.import_module(self.handler[self.path])

        attributes = dir(module)
        # check if was used core.Main class
        handlerMethod = None
        for attr in attributes:
            attribute = getattr(module, attr)
            if isinstance(attribute, type) and issubclass(attribute, core.Base):
                # define the handler
                handlerMethod = attribute()._run
                break

        handlerFunction = handlerMethod or getattr(module, function)
        # execute the handler
        handlerFunction()

    def _find_re_handler(self, path):
        """Checks if path match with any regular expression in self.handler.
        if true, return the key with regular expression, else return false.
        """
        for key in self.handler:
            if re.match(key, path):
                return key
        return False