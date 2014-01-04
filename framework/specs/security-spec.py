import os
import sys
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

import unittest
from unittest.mock import Mock
from framework import security


class StrFilter(unittest.TestCase):
    """docstring for KnownValues"""
    knownValues = (
        # Bocales
        ('AEIOU', 'aeiou'),
        # Bocales con acento
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('Á', 'a'),
        ('É', 'e'),
        ('Í', 'i'),
        ('Ó', 'o'),
        ('Ú', 'u'),
        # Bocales con acento grave
        ('à', 'a'),
        ('è', 'e'),
        ('ì', 'i'),
        ('ò', 'o'),
        ('ù', 'u'),
        ('À', 'a'),
        ('È', 'e'),
        ('Ì', 'i'),
        ('Ò', 'o'),
        ('Ù', 'u'),
        # Bocales con acento circunflejo
        ('â', 'a'),
        ('ê', 'e'),
        ('î', 'i'),
        ('ô', 'o'),
        ('û', 'u'),
        ('Â', 'a'),
        ('Ê', 'e'),
        ('Î', 'i'),
        ('Ô', 'o'),
        ('Û', 'u'),
        # Bocles con diéresis
        ('ä', 'a'),
        ('ë', 'e'),
        ('ï', 'i'),
        ('ö', 'o'),
        ('ü', 'u'),
        ('Ä', 'a'),
        ('Ë', 'e'),
        ('Ï', 'i'),
        ('Ö', 'o'),
        ('Ü', 'u'),
        # Eñe
        ('ñ', 'ni'),
        ('Ñ', 'ni'),
        # Special characters
        ('a b', 'a-b'),
        ('a  b', 'a-b'),
        ('a ', 'a'),
        ('a¿', 'a'),
        ('a   ? ', 'a'),
        ('a   - ', 'a'),
        ('¿?()/\\"\'ºª¡!|@·#~$%&¬/=^[]*+{}ç<>,;.:', ''),
        # numbers
        ('0123456789', '0123456789'),
        ('Título: ingeniero, edad: 26 años', 'titulo-ingeniero-edad-26-anios')
    )
    
    def test_str_filter(self):
        for specialCharacter, knownCaracter in self.knownValues:
            result = security.url_filter(specialCharacter)
            self.assertEqual(knownCaracter, result)


class set_absolute_pathTest(unittest.TestCase):
    """Test the set_absolute_path function. Here use the following
    nomenclature:
    http://     example.com     /~user_name   /any/path
       |            |               |            |
    protocol    server name      user name      path
    """
    def setUp(self):
        self.config = Mock()
        self.config.serverName = 'server.name'
        self.config.sharedSSLPath = 'shared.ssl/~username'

    def test_set_non_secure_path(self):
        """Should set an non secure path if the condition. Only fill the 
        path with the protocol, the server name and the 'request' string.
        """
        # See the condition:
        self.environ = {'HTTPS': None}
        self.config.enableSharedSSL = False
        self.config.enableHTTPS = False

        expected = 'http://server.name/request'

        obtained = security.set_absolute_path(
            'request', self.environ, self.config)
        self.assertEqual(expected, obtained)

    def test_set_secure_path(self):
        """Should set the secure protocol if the environ has the https key.
        Then set the server name and the path name ('request').
        """
        # See the condition:
        self.environ = {'HTTPS': 'yes'}
        self.config.enableSharedSSL = False
        self.config.enableHTTPS = False

        expected = 'https://server.name/request'

        obtained = security.set_absolute_path(
            'request', self.environ, self.config)
        self.assertEqual(expected, obtained)

    def test_set_secure_path_in_shared_ssl(self):
        """Here should complete the path with the shared ssl adress.
        """
        # See the condition:
        self.environ = {'HTTPS': 'yes'}
        self.config.enableSharedSSL = True
        self.config.enableHTTPS = False

        expected = 'https://shared.ssl/~username/request'
        
        obtained = security.set_absolute_path(
            'request', self.environ, self.config)
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()