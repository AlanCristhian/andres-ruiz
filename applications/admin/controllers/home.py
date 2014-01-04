from framework import core


class Admin(metaclass=core.Main):

    def handler(self):
        self.loggedTemplatePath = 'applications/admin/views/home.html'
        self.unloggedTemplatePath = 'applications/sharedHTML/unauthorized.html'
        self.logged(
            templatePath=self.loggedTemplatePath
            ,context={
                'title': 'Administrar'
                ,'contenido': 'contenido'
                ,'salir': True
            })
        self.unlogged(
            templatePath=self.unloggedTemplatePath
            ,context={
                'title': 'Sin permiso'
                ,'salir': False
            }
            ,status=401
        )