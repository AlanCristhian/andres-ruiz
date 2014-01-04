import os
import sys
import unittest
import sqlite3

from unittest.mock import Mock

oldDirectory = os.getcwd()
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

os.chdir(oldDirectory)
# from framework import test
import test


class testComponents(unittest.TestCase):
    def setUp(self):
        self.test = test.Test()

    def test_should_have_the_directory_property(self):
        self.test1 = test.Test()
        self.assertEqual(self.test1.directory, 'root')

        self.test2 = test.Test(directory='current')
        self.assertEqual(self.test2.directory, 'current')

        self.test3 = test.Test(directory='root')
        self.assertEqual(self.test3.directory, 'root')

    @unittest.skip('deprecated')
    def test_should_rayse_an_value_error(self):
        self.assertRaises(ValueError, test.Test, directory='not valid')     


if __name__ == '__main__':
    unittest.main()