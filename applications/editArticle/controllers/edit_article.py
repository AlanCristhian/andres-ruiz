from framework import core
from applications.helpers import helpers


class EditArticle(metaclass=core.Main):
    
    def setUp(self):
        self.templatePath = 'applications/editArticle/views/edit.html'
        self.unloggedTemplatePath = 'applications/sharedHTML/unauthorized.html'
        self.articles = self.serverCollection.get('articles')
        self.model = self.get_data()
        self.response.set_expires(0)

    def get_data(self):
        self.data = self.articles.get(
            where='edit_url=?'
            ,params=self.clientModel.url[1:].replace('~andresru/', '')
            ,format='dictList')
        return self.data[0] if self.data else {}

    def handler(self):
        self.logged_response(
            context={
                # convert the title to str to prevent fails when render it
                'title': str(self.model.get('title'))
                ,'salir': True}
            ,templatePath=self.templatePath)
        self.unlogged(
            templatePath=self.unloggedTemplatePath
            ,context={
                'title': 'Sin permiso'
                ,'salir': False}
            ,status=401)