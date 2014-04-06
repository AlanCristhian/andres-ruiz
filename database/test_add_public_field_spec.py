import unittest
from unittest.mock import Mock

from . import add_public_field
from framework import test
from framework import servermodel


class Test_AddPublicFiedl(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.new_field = add_public_field.AddPublicField(':memory:')

    def test_AddPublicField_class(self):
        self.assertHasAttr(add_public_field, 'AddPublicField')

    def test_collection_property(self):
        self.assertHasAttr(self.new_field, 'collection')

    def test_insert_public_field_method(self):
        self.assertHasAttr(self.new_field, 'insert_public_field')


if __name__ == '__main__':
    unittest.main()