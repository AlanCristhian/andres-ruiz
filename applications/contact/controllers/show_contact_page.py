from framework import core


class Main(metaclass=core.Main):

    def get_contact_info(self):
        self.contactCollection = self.serverCollection.get('contact')
        self.contactModel = self.contactCollection.get(
            where='id=?'
            ,params='1'
            ,format='dictList'            
        )
        if self.contactModel:
            self.contactInfo = self.contactModel[0]
        else:
            self.contactInfo = {}

    def handler(self):
        self.templatePath = 'applications/contact/views/index.html'
        self.get_contact_info()
        self.loggedContext = {
            'title': 'Información de contacto'
            ,'salir': True
            ,'model': self.contactInfo
        }
        self.unloggedContext = self.loggedContext.copy()
        self.unloggedContext['salir'] = False
        self.logged(
            context=self.loggedContext
            ,templatePath=self.templatePath
        )
        self.unlogged(
            context=self.unloggedContext
            ,templatePath=self.templatePath
        )