from urllib import parse

from framework import core
from framework import security


class ArticleCollection(metaclass=core.Main):
    """Send an list of dictionaries in text format.
    """
    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.article_list = self.articles.get(
            fields=('id', 'title', 'article_name', 'url', 'description',
                'public'),
            where='public=?',
            params=True,
            format='dictList',
        )
        self.multimedia = self.serverCollection.get('multimedia')
        self.update_fields()


    def get_first_paragraph(self, text):
        """Return the first paragraph of an text.
        """
        if text:
            if '\n' in text:
                return text.split('\n')[0]
            else:
                return text
        else:
            return None

    def update_fields(self):
        """Set the cover_description and the cover image.
        """
        auxiliarList = []
        for item in self.article_list:
            # get the first paragraph of the description
            item['description'] = self\
                .get_first_paragraph(item.pop('description'))
            # Get the url of the first image uploaded. The sqlite3 database
            # engine return the ascendent order by default.
            try:
                multimedia = self.multimedia.get(
                    fields=('url', 'type')
                    ,where='article_name=? AND cover=?'
                    ,params=(item.pop('article_name'), True)
                    ,format='dictList'
                )[0]
            except IndexError:
                multimedia = {}
                multimedia['url'] = None
                multimedia['type'] = None
            item['cover_image'] = multimedia['url']
            item['type'] = multimedia['type']



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
        self.basic_response(
            content=self.article_list,
            contentType='application/json',
        )
