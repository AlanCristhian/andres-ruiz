import os

import clientModel
import config
import helpers
import response
import security
import servermodel
import template
import session

settings = config.Config()
core = helpers.named_tuple({
    'session': session.Session()
    ,'clientModel': clientModel.Model()
    ,'config': settings
    ,'helpers': helpers
    ,'response': response.Response()
    ,'security': security
    ,'serverCollection': servermodel.Collection(settings.databasePath)
    ,'template': template.Render()
    ,'mkdir': os.mkdir
    ,'open': open
})

if not settings.production:
    from framework import coreMocks

    customMocks = coreMocks.CustomMocks()
    mocks = helpers.named_tuple({
        'session': customMocks.session.Session()
        ,'clientModel': customMocks.clientModel.Model()
        ,'config': customMocks.config.setup
        ,'helpers': helpers
        ,'response': customMocks.response.Response()
        ,'security': security
        ,'serverCollection': customMocks.serverCollection.Collection
        ,'template': customMocks.template.Template()
        ,'write': customMocks.write
        ,'mkdir': customMocks.mkdir
        ,'open': customMocks.open})