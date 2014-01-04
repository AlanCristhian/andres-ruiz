from unittest.mock import Mock
from unittest.mock import MagicMock
from framework import helpers


class CustomMocks:
    def __init__(self):
        # access
        self.access = Mock()
        self.access.validate = Mock(return_value={
            'result': {
                'templatePath': 'any/template/path',
                'context': {}
            }
        })

        # session
        self.session = Mock()
        self.session.Session = Mock()

        # config
        self.config = Mock()
        self.config.settings = {
            "production": False
            ,"consolelog": False
            ,"databaseEngine": "sqlite3"
            ,"databaseFolder": ":memory:/database"
            ,"filesFolder": ":memory:/files"
            ,"databaseFile": ":memory:"
            ,"databasePath": ":memory:"
            ,"cookieName": "sesid"
            ,"timeSession": "7 days"
            ,"securePath": "\/admin\/"
            ,"enableSharedSSL": False
            ,"sharedSSLDomain": "localhost"
            ,'sharedSSLUser': "/~username"
            ,"sharedSSLPath": "localhost/~username"
            ,"image": {
                "small": 64
                ,"medium": 128
                ,"large": 512
                ,"extralarge": 1024
            }
            ,"thumbnail": {
                "small": 32
                ,"medium": 64
                ,"large": 128
                ,"extralarge": 256
            }
            ,"minWidth": {
                "medium": "400"
                ,"large": "800"
                ,"extralarge": "1000"
            }
        }
        # self.config.setup = helpers.named_tuple(self.config.settings)
        self.config.setup = helpers.JavaScriptObject(self.config.settings)

        # helpers
        self.helpers = Mock()

        # clientModel
        self.Model = Mock()
        self.Model.get_form = Mock(return_value={}) # deprecated
        self.Model.form = {'key': 'value'}
        self.Model.get_url = Mock(return_value='http://www.example.com')
        self.Model.get_server_protocol = Mock(return_value='HTTP/1.1')
        # self.Model.get_cookie = Mock(return_value={})
        self.Model.cookie = {}
        self.Model.get_ip = Mock(return_value='1.2.3.4')

        self.clientModel = Mock()
        self.clientModel.Model = Mock(return_value=self.Model)

        # Response class
        self.Response = Mock()

        # Response class attributes
        self.Response.render = Mock(return_value='rendered text')
        self.Response.set_content_type = Mock()
        self.Response.get_content_type = Mock()
        self.Response.set_status = Mock()
        self.Response.set_charset = Mock()
        self.Response.set_expires = Mock()
        self.Response.redirect = Mock()
        self.Response.set_cookie = Mock()
        self.Response.set = Mock()

        # response module
        self.response = Mock()
        self.response.Response = Mock(return_value=self.Response)

        # serverModel
        self.serverModel = Mock()
        self.serverModel.get = Mock(return_value={})
        self.serverModel.update = Mock()

        # Collection
        self.Collection = Mock()
        self.Collection.get = Mock(return_value=[])

        # serverCollection
        self.serverCollection = Mock()
        self.serverCollection.Collection = Mock(return_value=self.Collection)
        self.serverCollection.Collection.has = Mock(return_value=False)
        self.serverCollection.Collection.get = Mock(return_value=self.serverModel)
        self.serverCollection.Collection.create = Mock()

        # Template class
        self.Template = Mock()
        self.Template.render = Mock(return_value='text rendered by template')

        # template module
        self.template = Mock()
        self.template.Template = Mock(return_value=self.Template)

        self.write = MagicMock()
        self.mkdir = Mock()
        self.open = MagicMock()