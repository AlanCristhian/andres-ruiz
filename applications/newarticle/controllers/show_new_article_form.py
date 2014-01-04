from framework import core


class NewArticleForm(metaclass=core.Main):

    def setUp(self):
        self.loggedTemplatePath = 'applications/newarticle/views/new_article_form.html'
        self.unloggedTemplatePath = 'applications/sharedHTML/unauthorized.html'

    def handler(self):
        self.logged(
            context={
                'title': 'Crear Nuevo Artículo'
                ,'salir': True}
            ,templatePath=self.loggedTemplatePath)
        self.unlogged(
            context={
                'title': 'Sin permiso'
                ,'salir': False}
            ,templatePath=self.unloggedTemplatePath
            ,status=401)