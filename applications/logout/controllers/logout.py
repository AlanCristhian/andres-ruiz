from framework import core


class Logout(metaclass=core.Main):

    def setUp(self):
        self.templatePath = 'applications/logout/views/logout.html'

    def handler(self):
        self.session.remove()
        self.basic_response(
            context={
                'title': 'Cerrando sesión'
                ,'salir': False}
            ,templatePath=self.templatePath
            ,expires=0)