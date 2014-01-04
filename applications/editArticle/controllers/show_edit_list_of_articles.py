from framework import core


class EditArticle(metaclass=core.Main):
    
    def setUp(self):
        self.templatePath = 'applications/editArticle/views/index.html'

    def handler(self):
        self.logged_response(
            context={
                'title': 'Editar artículo'
                ,'salir': True
            }
            ,templatePath=self.templatePath)