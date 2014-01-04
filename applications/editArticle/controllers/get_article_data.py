from framework import core
from applications.helpers import helpers


class GetData(metaclass=core.Main):

    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.articleURL = self.clientModel.form.get('edit_url')
        self.dataGroup = self.clientModel.form.get('data_group')
        self.response.set_expires(0)
        self.response.set_content_type('application/json')

    def get_data(self, method):
        if self.articleURL:
            self.data = method()
            if self.data:
                self.basic_response(content=self.data[0])
            else:
                self.basic_response(content={})
        else:
            self.basic_response(content={})

    def get_article_info(self):
        return self.articles.get(
            fields=('id', 'classification', 'country', 'state', 'city',
                    'autor', 'colaborators', 'project_date', 'article_name')
            ,where='edit_url=?'
            # Remove the bar "/" and add the shared ssl name if is an https
            # protocol and the sharedSSL variable is enabled in the
            # applications/settings.py config file.
            ,params=helpers.remove_user_name(self.articleURL[1:])
            ,format='dictList')

    def get_article_description(self):
        return self.articles.get(
            fields=('id', 'description')
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL[1:])
            ,format='dictList')

    def get_artile_cover(self):
        return self.articles.get(
            fields=('id', 'cover_image', 'cover_description')
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL[1:])
            ,format='dictList')

    def get_article_images(self):
        self.articleName = self.articles.get(
            fields='article_name'
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL[1:])
            ,distinct=True)
        self.images = self.serverCollection.get('images')
        return [self.images.get(
            fields=('id', 'url', 'description', 'classification')
            ,where='article_name=?'
            ,params=self.articleName[0]
            ,format='dictList')]

    def handler(self):
        if self.dataGroup == 'info':
            self.get_data(self.get_article_info)
        if self.dataGroup == 'description':
            self.get_data(self.get_article_description)
        if self.dataGroup == 'cover':
            self.get_data(self.get_artile_cover)
        if self.dataGroup == 'images':
            self.get_data(self.get_article_images)