from urllib import parse
import os

from framework import core
from framework import security

from applications.helpers import helpers


class GetArticleModel(metaclass=core.Main):
    """Response a JSON with all info of the article.
    """
    def setUp(self):
        # get the url of the article
        url = os.environ\
            .get('REQUEST_URI')\
            .replace('images/', '')
        self.article_URL = url[1:] if url[0] == '/' else url

        self.articles = self.serverCollection.get('articles')
        self.multimedia = self.serverCollection.get('multimedia')
        self.article_name = self.articles.get(
            fields='article_name'
            ,where='url=?'
            ,params=helpers.remove_user_name(self.article_URL)
            ,distinct=True)

    def get_multimedia(self):
        _database_result = self.multimedia.get(
            fields=('id', 'url', 'description', 'type', 'cover', 'article_name')
            ,where='article_name=?'
            ,params=self.article_name[0]
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

        return result

    def handler(self):
        if self.article_name:
            _content = self.get_multimedia()
            self.basic_response(
                content=_content,
                contentType='application/json',
            )
        else:
            self.basic_response(
                content={'error': self.article_URL + ' not exists'},
                contentType='application/json',
            )