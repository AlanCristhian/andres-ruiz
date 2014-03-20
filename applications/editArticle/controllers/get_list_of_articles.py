from urllib import parse

from framework import core
from framework import security


class ListOfArticles(metaclass=core.Main):
    """Response a list of articles."""
    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.article_list = self.articles.get(
            fields=('id', 'title', 'edit_url', 'article_name')
            ,format='dictList'
        )
        self.multimedia = self.serverCollection.get('multimedia')

    def get_first_paragraph(self, text):
        """Return the first paragraph of an text."""
        if '\n' in text:
            return text.split('\n')[0]
        else:
            return text

    def update_fields(self):
        auxiliarList = []
        for item in self.article_list:
            # Get the url of the first image uploaded. The sqlite3 database
            # engine return the ascendent order by default.
            try:
                result = self.multimedia.get(
                    fields=('url', 'type')
                    ,distinct=True
                    ,where='article_name=? AND cover=?'
                    ,params=(item['article_name'], True)
                    ,format='dictList'
                )[0]
                url = result['url']
                multimedia_type = result['type']
            except IndexError:
                url = ''
                multimedia_type = None
            item['cover_image'] = url
            item['type'] = multimedia_type

            # add the hostname and the protocol to the url if is an file path
            if item['type'] == 'image_file':
                item['cover_image'] = security \
                    .set_absolute_path(item['cover_image'])

            # add the video id key if is an youtube video
            elif item['type'] == 'video_link':
                url_tuple = parse.urlparse(item['cover_image'])
                queries = parse.parse_qs(url_tuple.query)
                if queries.get('v'):
                    item['vid'] = queries['v'][0]
                else:
                    item['vid'] = ''
            auxiliarList = auxiliarList + [item]
        # update all fields
        self.article_list = auxiliarList


    def handler(self):
        self.update_fields()
        self.logged_response(
            content=self.article_list
            ,contentType='application/json'
        )