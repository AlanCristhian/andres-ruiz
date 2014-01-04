from framework import core


class Error404(metaclass=core.Main):

    def handler(self):
        self.templatePath = 'applications/error/error404.html'
        self.unlogged(
            context={
                'url': self.clientModel.url
                ,'title': '404 No encontrado'
                ,'salir': False}
            ,templatePath=self.templatePath
            ,status=404)
        self.logged(
            context={
                'url': self.clientModel.url
                ,'title': '404 No encontrado'
                ,'salir': True}
            ,templatePath=self.templatePath
            ,status=404)