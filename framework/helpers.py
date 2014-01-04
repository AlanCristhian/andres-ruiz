import collections
import datetime
import json
import os
import uuid


def get_datetime(delta=None):
    """Returns the current date in a standard format.
    You could also set a delta parameter."""
    if delta:
        return datetime.datetime.today() + datetime.timedelta(seconds=delta)
    else:
        return datetime.datetime.today()


class Singleton(type):
    """Implements the singleton design pattern.
    """
    def __init__(cls, name, bases, namespace, **kwds):
        cls.__instance = None
        type.__init__(cls, name, bases, namespace, **kwds)
 
    def __call__(cls, *args, **kwds):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kwds)
        return cls.__instance


class Flyeight(type):
    """Implements the flyeight design pattern.
    """
    def __init__(cls, name, bases, namespace, **kwds):
        cls.__instances = {}
        type.__init__(cls, name, bases, namespace, **kwds)
 
    def __call__(cls, key, *args, **kwds):
        instance = cls.__instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kwds)
            cls.__instances[key] = instance
        return instance


def get_protocol():
    """return the protocol"""
    protocol = os.environ.get('REDIRECT_HTTPS')
    return 'https' if protocol else 'http'


def named_tuple(dictionary):
    """return an namedtuple object make with the dictionary"""
    Data = collections.namedtuple('Data', dictionary.keys())
    return Data(**dictionary)


class JavaScriptObject(dict):
    """The attribute can be referenced by indexing (e.g. d[name])
    or by directly using the dot (.) operator (e.g. d.name)."""
    def __init__(self, *args, **kwargs):
        self.update(*args)
        self.update(**kwargs)

    def __getattr__(self, name):
        return self[name]
            
    def __setattr__(self, name, value):
        self[name] = value


# Recipe created by Oren Tirosh on Thu, 2 Aug 2012 (MIT)
# http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
def memodict(function):
    """Memorization decorator for a function taking a single argument."""
    class memodict(dict):
        def __missing__(self, key):
            result = self[key] = function(key)
            return result
    return memodict().__getitem__


def variable_name(obj, namespace):
    "Get an str object with the variable name of the obj."
    for name in namespace:
        if namespace[name] is obj:
            return name


def alpha_uuid():
    """Make an Universally Unique IDentifier (UUID) in alphanumeric format."""
    number = uuid.uuid4().int
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    result = ''
    length = 62
    while number:
        result = chars[number % length] + result
        number = number // length
    return result
