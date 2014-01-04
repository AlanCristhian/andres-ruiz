try:
    from framework import core
    class CustomClass(metaclass=core.Main):
        pass
except:
    pass

def function():
    return 'this is a function'

def handler():
    return 'this is an default function'

def custom():
    return 'this is an custom function'