import datetime

from framework import core


class NewArticle(metaclass=core.Main):

    def setUp(self):
        self.response.set_content_type('application/json')
        self.form = self.clientModel.form
        self.clientArticleName = self.security.url_filter(
            self.form.get('article_name'))
        self.serverArticleName = self.get_article_name()
        self.articlePath = self.config.filesFolder + '/' \
                         + self.clientArticleName + '-folder'
        self.editURL = 'admin/editar/' + self.clientArticleName

    def get_article_name(self):
        self.articles = self.serverCollection.get('articles')
        return self.articles.get(
            where='article_name=?'
            ,params=self.clientArticleName)

    def create_article(self):
        self.date = datetime.datetime.today()
        self.articles.insert(
            article_name=self.clientArticleName
            ,title=self.form.get('article_name')
            ,url=self.clientArticleName
            ,edit_url=self.editURL
            ,creation_date=self.date
            ,last_modified=self.date
            ,directory=self.articlePath)
        self.mkdir(self.articlePath)
        return True

    def handler(self):
        if self.serverArticleName:
            self.logged(content={'exists': True})
        elif self.create_article():
            self.logged(content={'status': True, 'edit_url': self.editURL})
        else:
            self.logged(content={'status': False})
