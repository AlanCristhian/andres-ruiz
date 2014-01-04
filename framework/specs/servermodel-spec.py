import os
import sys
import unittest

from unittest.mock import Mock

oldDirectory = os.getcwd()
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from framework import servermodel
from framework import config
os.chdir(oldDirectory)


class CollectionTest(unittest.TestCase):
    def setUp(self):
        self.collection = servermodel.Collection(':memory:')

    def test_should_be_has_database_path_method(self):
        self.assertTrue(hasattr(self.collection, 'path'))

    def test_should_be_return_database_path(self):
        expected = ':memory:'
        obtained = self.collection.path()
        self.assertTrue(expected, obtained)

    # def test_should_raise_NotImplementedError(self):
    #     settings = Mock()
    #     settings.databaseEngine = 'any'
    #     config.Config = Mock(return_value=settings)
    #     serverCollection.Collection(':memory:', dbengine)
    #     print(config.Config().databaseEngine)
        # self.assertRaises(NotImplementedError, serverCollection.Collection, ':memory:')


if __name__ == '__main__':
    unittest.main()