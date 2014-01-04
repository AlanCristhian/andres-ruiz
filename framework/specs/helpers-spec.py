import test
import unittest
from unittest.mock import Mock
import helpers


class NamedTupleTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.example = {
            'number': 12345
            ,'text': 'Hello world'
        }
        self.namedTuple = helpers.named_tuple(self.example)

    def test_should_has_number_attribute(self):
        self.assertHasAttr(self.namedTuple, 'number')

    def test_should_has_text_attribute(self):
        self.assertHasAttr(self.namedTuple, 'text')

    def test_should_get_number_value(self):
        self.assertEqual(self.namedTuple.number, 12345)

    def test_should_get_text_value(self):
        self.assertEqual(self.namedTuple.text, 'Hello world')


class JavaScriptObjectTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.dict = {'a': 'firsth letter', 'b': 'second letter'}
        self.object = helpers.JavaScriptObject(self.dict)

    def test_should_has_a_attribute(self):
        self.assertHasAttr(self.object, 'a')

    def test_should_get_b_value(self):
        self.assertEqual(self.object.b, 'second letter')

    def test_shoul_raise_an_AttributeError(self):
        self.assertRaises(KeyError, lambda x: self.object[x], 'c')


class variable_nameTest(unittest.TestCase, test.CustomAssertions):
    def test_should_return_the_name_of_variable(self):
        variable = 'any variable'
        obtained = helpers.variable_name(variable, locals())
        expected = 'variable'
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()