import unittest
import test
from applications.error import error404


class Error404Components(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.error = error404.Error404(dependencies=test.mocks)
        self.error.handler()

    def test_should_exist_template_path(self):
        self.assertFileExists(self.error.templatePath)


if __name__ == '__main__':
    unittest.main()