import unittest
from framework import test
from framework import config


class ConfigComponents(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.config = config.Config()

    def test_should_have_all_attributes(self):
        self.assertHasAttr(self.config, 'production')
        self.assertHasAttr(self.config, 'consolelog')
        self.assertHasAttr(self.config, 'serverName')
        self.assertHasAttr(self.config, 'databaseEngine')
        self.assertHasAttr(self.config, 'databaseFolder')
        self.assertHasAttr(self.config, 'databasePath')
        self.assertHasAttr(self.config, 'databaseFile')
        self.assertHasAttr(self.config, 'cookieName')
        self.assertHasAttr(self.config, 'timeSession')
        self.assertHasAttr(self.config, 'securePath')
        self.assertHasAttr(self.config, 'image')
        self.assertHasAttr(self.config, 'thumbnail')
        self.assertHasAttr(self.config, 'minWidth')
        # self.assertHasAttr('', self.config)

    def test_should_exists_a_database_file(self):
        self.assertFileExists(self.config.databasePath)


if __name__ == '__main__':
    unittest.main()