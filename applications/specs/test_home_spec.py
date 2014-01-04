import unittest
from unittest.mock import Mock
import test
from applications.home.controllers import home


class HomeSpec(unittest.TestCase, test.CustomAssertions):
    """Test for the module that show a page with the default data.
    """
    def setUp(self):
        self.home = home.HomeHandler()

    def test_HomeHandler_instance(self):
        """Would be able to create an instance of HomeHandler class.
        """
        self.assertIsInstance(self.home, home.HomeHandler)

    def test_template_existence(self):
        """The template should exists in the disc.
        """
        self.assertFileExists(self.home.templatePath)

    def test_response_with_single_info(self):
        """Should send a response with the single data.
        """
        self.home.basic_response = Mock()
        self.home.handler()
        self.home.basic_response.assert_called_with(
            templatePath=self.home.templatePath,
            context={
                'title': 'Home',
                'description': 'Página principal de andresnorbertoruiz.com',
                'salir': False
            },
        )


if __name__ == '__main__':
    unittest.main()