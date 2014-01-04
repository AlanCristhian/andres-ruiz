import shutil

from framework import core


class RemoveArticle(metaclass=core.Main):
    """The app that hadle the article removal."""
    def setUp(self):
        if self.session.validate():
            self.response.set_content_type('application/json')
            self.form = self.clientModel.form;
            self.title = self.form.get('title')
            self.id = self.form.get('id')
            self.articles = self.serverCollection.get('articles')
            
    def rmtree(self, path, ignore_errors=False, onerror=None):
        """Delete an entire directory tree.
        I set this alias to alow mocking.
        """
        return shutil.rmtree(path, ignore_errors, onerror)

    def remove_article(self):
        self.articleDirectory =  self.articles.get(
            fields='directory'
            ,where='id=?'
            ,params=self.id
            ,format='strList'
        )[0]
        self.articles.remove(where='id=?', params=self.id)
        self.rmtree(self.articleDirectory)


    def handler(self):
        if self.session.validate():
            self.remove_article()
            self.logged_response(
                content={'status': 'The article ' + self.title + ' whas removed.'}
            )
        else:
            self.logged_response(
                content={'status': 'you not permission.'}
            )