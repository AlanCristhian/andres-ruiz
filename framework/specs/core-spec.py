import unittest
from unittest.mock import Mock


from framework import test
from framework import core
from framework import dependencies


class coreSpec(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.core = core.Base(dependencies=dependencies.mocks)

    def test_has_all_methods(self):
        self.assertHasAttr(self.core, '_parse')
        self.assertHasAttr(self.core, '_run')
        # self.assertHasAttr(self.core, 'on')
        # self.assertHasAttr(self.core, 'trigger')
        # self.assertHasAttr(self.core, 'off')
        self.assertHasAttr(self.core, 'handler')
        self.assertHasAttr(self.core, 'mkdir')
        self.assertHasAttr(self.core, 'open')
        self.assertHasAttr(self.core, 'write')
        self.assertHasAttr(self.core, 'setUp')
        self.assertHasAttr(self.core, 'tearDown')

    def test_raise_type_error(self):
        self.core.handler = lambda: 'any text'
        self.assertRaises(TypeError, self.core.handler())

    def test_write_unloged_result(self):
        self.core.handler = lambda: {
            'content': 'any text'
        }
        self.core._parse()
        self.assertEqual(self.core._result, 'rendered text')

    def test_call_any_response_method(self):
        self.core.handler = lambda: {
            'content': 'any text'
            ,'status': '200'
        }
        self.core._parse()
        self.core.response.set.assert_called_with('status', '200')

    def test_raise_key_error(self):
        self.core.handler = lambda: {
            'not valid key': 'any text'
        }
        self.assertRaises(KeyError, self.core._parse)
        self.core.handler = lambda: {
            'logged': 'any text'
        }
        self.assertRaises(KeyError, self.core._parse)
        self.core.handler = lambda: {
            'unlogged': 'any text'
        }
        self.assertRaises(KeyError, self.core._parse)

    def test_response_a_string(self):
        self.core.handler = lambda: {
            'content': 'any text'
        }
        self.core._execute_response_methods = Mock()
        self.core._parse()
        self.assertEqual(self.core._result, 'rendered text')
        self.assertCalled(self.core._execute_response_methods)

    def test_response_a_json(self):
        self.core.handler = lambda: {
            'content': {}
            ,'contentType': 'application/json'
        }
        self.core._execute_response_methods = Mock()
        self.core._parse()
        self.assertEqual(self.core._result, 'rendered text')
        self.assertCalled(self.core._execute_response_methods)

    def test_render_a_template_and_response_a_sting(self):
        handler_value = {
            'context': {}
            ,'templatePath': 'any/path'
            ,'contentType': 'application/json'
        }
        self.core._execute_response_methods = Mock()
        self.core.handler = lambda: handler_value
        self.core._parse()
        self.core.template.render.assert_called_with({
            'context': {}
            ,'templatePath': 'any/path'
            ,'contentType': 'application/json'
        })
        self.assertCalled(self.core._execute_response_methods)

    def test_validate_content(self):
        handler_value = {
            'unlogged': {
                'templatePath': ''
                ,'context': ''
                ,'status': ''
                ,'contentType': 'json'
                ,'charset': ''
                ,'expires': ''
                ,'redirect': ''
                ,'cookie': ''
            }
            ,'logged': {
                'templatePath': ''
                ,'context': ''
                ,'status': ''
                ,'contentType': 'json'
                ,'charset': ''
                ,'expires': ''
                ,'redirect': ''
                ,'cookie': ''
            }
        }
        self.core._execute_response_methods = Mock()
        self.core.handler = lambda: handler_value
        self.core._parse()
        self.assertTrue(self.core.session.validate.called)
        self.assertCalled(self.core._execute_response_methods)

    def test_raise_KeyError_when_validate(self):
        handler_value = {
            'unlogged': {
                'context': ''
                ,'status': ''
                ,'contentType': 'json'
                ,'charset': ''
                ,'expires': ''
                ,'redirect': ''
                ,'cookie': ''
            }
            ,'logged': {
                'context': ''
                ,'status': ''
                ,'contentType': 'json'
                ,'charset': ''
                ,'expires': ''
                ,'redirect': ''
                ,'cookie': ''
            }
        }
        self.core.handler = lambda: handler_value
        self.assertRaises(KeyError, self.core._parse)

    def test_compose_product(self):
        self.core.handler = lambda: None
        self.core._compose = Mock(return_value={
            'logged': {'content': ''}
            ,'unlogged': {'content': ''}
        })
        self.core._parse()
        self.assertCalled(self.core._compose)

    def test_to_be_a_subclass_of_main(self):
        class Main(metaclass=core.Main):
            def handler(self):
                pass
        self.assertIsSubclass(Main, core.Base)

    def test_raise_a_DefaultAttributeWarning(self):
        def assign(value):
            self.core.template = value
        self.assertWarns(
            core.DefaultAttributeWarning
            ,assign
            ,'any value'
        )

    def test_raise_a_TypeAttributeWarning(self):
        class Main(metaclass=core.Main):
            def any_method(self, name, age):
                self.name = name
                self.name = age
        main = Main(dependencies=dependencies.mocks)
        self.assertWarns(
            core.TypeAttributeWarning
            ,main.any_method
            ,'alan', 27
        )

    def test_raise_a_NamespaceWarning(self):
        class Main(metaclass=core.Main):
            def any_method(self):
                variable_local = 'this is place into local namespace'
                self.variable = 'this is place into self namespace'
        main = Main(dependencies=dependencies.mocks)
        self.assertWarns(core.NamespaceWarning, main.any_method)

    def test_not_raise_a_NamespaceWarning(self):
        class Main(metaclass=core.Main):
            def any_method(self):
                variable_local = 'this is place into local namespace'
                self.variable = 'this is place into self namespace'
        main = Main(dependencies=dependencies.mocks, warnings=None)
        main.any_method()
        self.assertWarns(core.NamespaceWarning, main.any_method)

    def test_add_setUp_and_tearDown_methods_to_handler(self):
        class Main(metaclass=core.Main):
            pass
        main = Main(dependencies=dependencies.mocks)
        main.setUp = Mock()
        main.tearDown = Mock()
        main.handler()
        self.assertTrue(main.setUp.called)
        self.assertTrue(main.tearDown.called)

    def test_response_a_basic_response_string(self):
        self.core.handler = lambda: None
        self.core.simple_response = Mock()
        self.core._simple = {
            'content': 'rendered text'
        }
        self.core._parse()
        self.assertEqual(self.core._result, 'rendered text')


if __name__ == '__main__':
    unittest.main()