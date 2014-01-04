from framework import core


class Contact(metaclass=core.Main):

    def setUp(self):
        self.templatePath = 'applications/editContact/views/index.html'
        self.unauthorized = 'applications/sharedHTML/unauthorized.html'

    def handler(self):
        self.logged(
            context={
                'title': 'Información de contacto'
                ,'salir': True}
            ,templatePath=self.templatePath)
        self.unlogged(
            context={
                'title': 'Sin permiso'
                ,'salir': False}
            ,templatePath=self.unauthorized)