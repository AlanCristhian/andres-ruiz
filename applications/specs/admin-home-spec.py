import unittest
import test
from applications.admin.controllers import home


class AdminComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.admin = home.Admin(dependencies=test.mocks)

    def test_should_exists_unlogged_template_file(self):
        self.assertFileExists('applications/sharedHTML/unauthorized.html')

    def test_should_exists_logged_template_file(self):
        self.assertFileExists('applications/admin/views/home.html')


if __name__ == '__main__':
    unittest.main()