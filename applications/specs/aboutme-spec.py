import unittest
import test
from applications.aboutme.controllers import aboutme


class AboutMeCompents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.about = aboutme.About(dependencies=test.mocks)

    def test_should_to_be_an_type_instance(self):
        self.assertIsInstance(self.about, aboutme.About)

    def test_should_exists_template_file(self):
        self.assertFileExists('applications/aboutme/views/index.html')


if __name__ == '__main__':
    unittest.main()