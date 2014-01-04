import warnings as _warnings
import inspect
import sys

from framework.dependencies import core


# Custom warning class
class DefaultAttributeWarning(Warning): pass
class TypeAttributeWarning(Warning): pass
class NamespaceWarning(Warning): pass


class Base:
    def __init__(self,
        dependencies=core
        ,warnings=True
    ):
        # disable warnings with not raise this when set dependencies
        self._warnings = False
        self.session = dependencies.session
        self.clientModel = dependencies.clientModel
        self.config = dependencies.config
        self.helpers = dependencies.helpers
        self.response = dependencies.response
        self.security = dependencies.security
        self.serverCollection = dependencies.serverCollection
        self.template = dependencies.template
        self.mkdir = dependencies.mkdir
        self.open = dependencies.open

        self._result = ''
        self.default_attr = self.__dict__.copy()
        self.valid_attr = {'_result', 'handler', '_warnings', '_logged',
            '_unlogged', '_basic'}

        # decorate handler method
        self.handler = self._add_setUp_and_tearDown(self.handler)

        self._logged = self._unlogged = {'content': ''}
        self._basic = {}

        # config warnings
        self.warnings = True if warnings else False

    @property
    def warnings(self):
        return self._warnings

    @warnings.setter
    def warnings(self, value: bool):
        if value == True:
            _warnings.simplefilter('default')
        else:
            _warnings.simplefilter('ignore')
        self._warnings = value

    def setUp(self):
        "method for setting up the class fixture before run handler method."
        pass

    def tearDown(self):
        "method for deconstructing the class fixture after run handler method."
        pass

    def handler(self):
        ""
        pass

    def logged(self, **kwds):
        self._logged = kwds

    def unlogged(self, **kwds):
        self._unlogged = kwds

    def logged_response(self, **kwds):
        self._logged = kwds

    def unlogged_response(self, **kwds):
        self._unlogged = kwds

    def basic_response(self, **kwds):
        self._basic = kwds

    def write(self, buffer_, end=''):
        """Send the response to the user browser.
        """
        sys.stdout.buffer.write(bytes(buffer_, self.response.encoding))

    def _execute_response_methods(self, value):
        product = {}
        product.update(value)
        if 'content' in product:
            product.pop('content')
        if 'context' and 'templatePath' in product:
            product.pop('context')
            product.pop('templatePath')
        for key in product:
            self.response.set(key, product[key])

    def _compose(self):
        return {'logged': self._logged, 'unlogged': self._unlogged}


    def _parse(self):
        product = self.handler()
        if not product:
            product = self._basic if self._basic else self._compose()
        if isinstance(product, dict): # is an dictionary
            # is an simple response
            if 'content' in product:
                content = product.get('content')
                self._execute_response_methods(product)
                self._result = self.response.render(content)

            # simple response with template and context
            elif 'context' and 'templatePath' in product:
                render = self.template.render(product)
                self._execute_response_methods(product)
                self._result = self.response.render(render)

            # have private info
            elif 'logged' in product\
            and 'unlogged' in product:
                if self.session.validate():
                    validatedData = product['logged']
                    status = 'logged'
                else:
                    validatedData = product['unlogged']
                    status = 'unlogged'

                # is an simple response
                if 'content' in validatedData:
                    content = validatedData.get('content')
                    self._execute_response_methods(validatedData)
                    self._result = self.response.render(content)

                # simple response with template and context
                elif 'context' and 'templatePath' in validatedData:
                    render = self.template.render(validatedData)
                    self._execute_response_methods(validatedData)
                    self._result = self.response.render(render)
                else:
                    raise KeyError(
                        'Te keys in into "' + status + '" must be "content"' \
                        + 'or "context" and "templatePath".')
            else:
                raise KeyError(
                    'Te keys in the value return for handler() method must '\
                    'be "content" or "unlogged" and "logged".')
        else: # is not a dictionary
            raise TypeError(
                'The handler() method must be return an dict object or call '\
                'logged() and unlogged() methods')

    def _run(self):
        self._parse()
        # Print the response without the carriage return. This
        # is to avoid problems with ajax and the plaintext.
        self.write(self._result, end='')

    def __setattr__(self, name, value):
        if hasattr(self, '_warnings') and hasattr(self, 'default_attr'):
            if self._warnings:
                defaultAttributeMessage = '"{name}" is an default attribute of '\
                    'core.Base class. If you replace it, you might have problems '\
                    'with the execution of the handler.'
                typeAttributeMessage = 'The previous value of this attribute "{value}" '\
                    'is type {previous}. The new value is type {actual}.'
                if name in self.default_attr:
                    if name not in self.valid_attr:
                        _warnings.warn(
                            defaultAttributeMessage.format(name=name)
                            ,DefaultAttributeWarning
                            ,stacklevel=2)
                elif name in self.__dict__:
                    if name not in self.valid_attr:
                        previousType = type(self.__dict__[name])
                        actualType = type(value)
                        if previousType != actualType:
                            _warnings.warn(
                                typeAttributeMessage.format(
                                    previous=previousType
                                    ,actual=actualType
                                    ,value=self.helpers.variable_name(value, locals()))
                                ,TypeAttributeWarning
                                ,stacklevel=2)
        super().__setattr__(name, value)

    def _add_setUp_and_tearDown(self, function):
        def inner(*args):
            self.setUp()
            result = function(*args)
            self.tearDown()
            return result
        return inner


class Main(type):
    def __new__(cls, name, bases, namespace, **kwds):
        """Returns a new class that inherits from main"""
        extendedBases = bases + (Base,)
        result = super().__new__(cls, name, extendedBases, namespace)
        for attribute, value in namespace.items():
            if '__' not in attribute \
            and callable(value):
                setattr(result, attribute, cls.add_namespace_warning(value))
        return result

    @classmethod
    def add_namespace_warning(cls, function):
        def inner(*args):
            arguments = set(inspect.getfullargspec(function).args)
            variables = set(function.__code__.co_varnames)
            localVariable = variables.difference(arguments)
            if localVariable:
                namespaceWarning = 'The contents of the variable "{name}" can'\
                    ' not be tested. You should use "{self}.{name}" '\
                    'to access this value during testing.'
                _warnings.warn(
                    namespaceWarning.format(
                        self=tuple(arguments)[0]
                        ,name=tuple(localVariable)[0])
                    ,NamespaceWarning
                    ,stacklevel=2)
            return function(*args)
        return inner