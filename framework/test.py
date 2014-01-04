"""This library involves common tasks for testing"""


import os
from unittest.mock import Mock
from unittest.mock import MagicMock


class CustomAssertions:
    def assertFileExists(self, path):
        if not os.path.lexists(path):
            raise AssertionError('File not exists in path "' + path + '".')

    def assertHasAttr(self, object_, name):
        if not hasattr(object_, name):
            raise AssertionError(object_.__class__.__name__ + \
                " object has no attribute '" + name + "'.")

    def assertIsSubclass(self, A, B):
        if not issubclass(A, B):
            raise AssertionError(
                str(A) + ' object is not a subclass of ' + str(B) + '.')

    def assertCalled(self, function):
        if callable(function):
            if isinstance(function, Mock) or isinstance(function, MagicMock):
                if not function.called:
                    raise AssertionError('Not called.')
            else:
                raise TypeError(
                    'The object must be an instance of Mock or MagicMock')
        else:
            raise AssertionError('The object is not callable.')

    
    # TODO: find a way to test that the handler exists