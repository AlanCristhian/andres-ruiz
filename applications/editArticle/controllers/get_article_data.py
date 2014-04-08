from urllib import parse

from framework import core
from framework import security

from applications.helpers import helpers


class GetData(metaclass=core.Main):

    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        url = self.clientModel.form.get('edit_url')
        # remove initial slash
        self.articleURL = url = url[1:] if url[0] == '/' else url
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
                    'autor', 'colaborators', 'project_date', 'article_name',
                    'public', 'title')
            ,where='edit_url=?'
            # Remove the bar "/" and add the shared ssl name if is an https
            # protocol and the sharedSSL variable is enabled in the
            # applications/settings.py config file.
            ,params=helpers.remove_user_name(self.articleURL)
            ,format='dictList')

    def get_article_description(self):
        return self.articles.get(
            fields=('id', 'description')
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL)
            ,format='dictList')

    def get_artile_cover(self):
        return self.articles.get(
            fields=('id', 'cover_image', 'cover_description')
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL)
            ,format='dictList')

    def get_article_multimedia(self):
        self.articleName = self.articles.get(
            fields='article_name'
            ,where='edit_url=?'
            ,params=helpers.remove_user_name(self.articleURL)
            ,distinct=True)
        self.multimedia = self.serverCollection.get('multimedia')
        _database_result = self.multimedia.get(
            fields=('id', 'url', 'description', 'type', 'cover', 'article_name')
            ,where='article_name=?'
            ,params=self.articleName[0]
            ,format='dictList')
        result = []
        for item in _database_result:
            # add the hostname and the protocol to the url if is an file path
            if item['type'] == 'image_file':
                item['url'] = security.set_absolute_path(item['url'])

            # add the video id key if is an youtube video
            elif item['type'] == 'video_link':
                url_tuple = parse.urlparse(item['url'])
                queries = parse.parse_qs(url_tuple.query)
                # check if the url have the 'v' key
                if queries.get('v'):
                    item['vid'] = queries['v'][0]
                else:
                    item['vid'] = ''
            result.append(item)

        return [result]

    def handler(self):
        if self.dataGroup == 'info':
            self.get_data(self.get_article_info)
        if self.dataGroup == 'description':
            self.get_data(self.get_article_description)
        if self.dataGroup == 'cover':
            self.get_data(self.get_artile_cover)
        if self.dataGroup == 'multimedia':
            self.get_data(self.get_article_multimedia)