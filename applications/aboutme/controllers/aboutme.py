from framework import core


class About(metaclass=core.Main):

    def handler(self):
        self.logged(
            context={
                'title': 'Sobre mí'
                ,'salir': True
            }
            ,templatePath='applications/aboutme/views/index.html'
        )
        self.unlogged(
            context={
                'title': 'Sobre mí'
                ,'salir': False
            }
            ,templatePath='applications/aboutme/views/index.html'
        )