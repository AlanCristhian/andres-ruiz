import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock

from framework import test
from framework import clientModel


class ClientModelComponets(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.clientModel = clientModel.Model()

    def test_instantiate_clientModel(self):
        self.assertIsInstance(self.clientModel, clientModel.Model)

    def test_has_form_property(self):
        self.assertHasAttr(self.clientModel, 'form')

    def test_has_cookie_property(self):
        self.assertHasAttr(self.clientModel, 'cookie')

    def test_has_url_property(self):
        self.assertHasAttr(self.clientModel, 'url')

    def test_has_serverProtocol_property(self):
        self.assertHasAttr(self.clientModel, 'serverProtocol')

    def test_has_protocol_property(self):
        self.assertHasAttr(self.clientModel, 'protocol')

    def test_has_ip_property(self):
        self.assertHasAttr(self.clientModel, 'ip')

    def test_has_ip_property(self):
        self.assertHasAttr(self.clientModel, 'desktopSession')


if __name__ == '__main__':
    unittest.main()