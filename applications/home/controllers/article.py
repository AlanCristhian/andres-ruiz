from framework import core
from applications.helpers import helpers


class Article(metaclass=core.Main):
    """Show the info of an individual article.
    """

    def get_articles(self):
        """Return a lis of articles fields"""
        self.article = self.serverCollection.get('articles')
        if hasattr(self.clientModel, 'https') \
        and self.config.enableSharedSSL:
            self.article_URL = self.clientModel.url.replace('/~andresru/proyectos/', '')
        else:
            self.article_URL = self.clientModel.url.replace('/proyectos/', '')
        # get fields
        return self.article.get(
            fields=(
                'article_name'
                ,'title'
                ,'description'
                ,'url'
                ,'classification'
                ,'country'
                ,'state'
                ,'city'
                ,'autor'
                ,'colaborators'
                ,'project_date')
            ,where='url=?'
            ,params=self.article_URL
            ,distinct=True
            ,format='dictList')

    def handler(self):
        # get fields
        self._articlesList = self.get_articles()
        if self._articlesList:
            # format all paragraphs
            self._articlesList[0]['description'] = helpers.paragraph_filter(
                self._articlesList[0]['description']
            )

            self.projectDict = self._articlesList[0]
            self.loggedContext = {
                'title': self.projectDict.get('title')
                ,'description': self.projectDict.get('description')
                ,'salir': True
                ,'classification': self.projectDict.get('classification')
                ,'country': self.projectDict.get('country')
                ,'state': self.projectDict.get('state')
                ,'city': self.projectDict.get('city')
                ,'autor': self.projectDict.get('autor')
                ,'colaborators': self.projectDict.get('colaborators')
                ,'project_date': self.projectDict.get('project_date')
            }
            self.loggedTemplatePath = 'applications/home/views/article.html'
            self.unloggedTemplatePath = self.loggedTemplatePath
            self.unloggedContext = self.loggedContext.copy()
            self.unloggedContext['salir'] = False
            self.logged(
                context=self.loggedContext
                ,templatePath=self.loggedTemplatePath
            )
            self.unlogged(
                context=self.unloggedContext
                ,templatePath=self.unloggedTemplatePath
            )
        # launch 404 error if url is not found
        else:
            self.loggedContext = {
                'url': self.clientModel.url
                ,'title': '404 No encontrado'
                ,'salir': True}
            self.loggedTemplatePath = 'applications/error/error404.html'
            self.unloggedTemplatePath = self.loggedTemplatePath
            self.unloggedContext = self.loggedContext.copy()
            self.unloggedContext['salir'] = False
            self.response.set_status(404)
            self.logged(
                context=self.loggedContext
                ,templatePath=self.loggedTemplatePath
            )
            self.unlogged(
                context=self.unloggedContext
                ,templatePath=self.unloggedTemplatePath
            )