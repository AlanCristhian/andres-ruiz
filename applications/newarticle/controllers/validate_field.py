from framework import core


class Validate(metaclass=core.Main):
    
    def setUp(self):
        self.form = self.clientModel.form
        self.response.set_content_type('application/json')

    def get_articles_model(self):
        return self.serverCollection.get('articles')

    def handler(self):
        if 'article_name' in self.form:
            self.articles = self.get_articles_model()
            self.clientName = \
                (self.security.url_filter(self.form['article_name']),)
            self.serverNames = self.articles.get('article_name')
            if self.clientName in self.serverNames:
                self.basic_response(content={'exists': True})
            else:
                self.basic_response(content={'exists': False})
        else:
            self.basic_response(
                content='No existe ese campo'
                ,contentType='text/plain')