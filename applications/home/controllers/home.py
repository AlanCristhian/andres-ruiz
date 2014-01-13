from framework import core


class HomeHandler(metaclass=core.Main):
    """Send a list whit info of all articles.
    """
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.templatePath = 'applications/home/views/home.html'

    def handler(self):
        self.basic_response(
            templatePath=self.templatePath,
            context={
                'title': 'Home',
                'description': 'Página principal de andresnorbertoruiz.com',
                'salir': False,
            },
        )
