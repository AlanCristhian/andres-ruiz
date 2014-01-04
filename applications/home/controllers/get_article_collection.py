from framework import core


class ArticleCollection(metaclass=core.Main):
    """Send an list of dictionaries in text format.
    """
    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.article_list = self.articles.get(
            fields=('id', 'title', 'article_name', 'url', 'description'),
            format='dictList',
        )
        self.images = self.serverCollection.get('images')
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
                url = self.images.get(
                    fields='url'
                    ,where='article_name=?'
                    ,params=item.pop('article_name')
                    ,format='strList'
                )[0]
            except:
                url = ''
            item['cover_image'] = url
            auxiliarList = auxiliarList + [item]
        # update all fields
        self.article_list = auxiliarList

    def handler(self):
        self.basic_response(
            content=self.article_list,
            contentType='application/json',
        )
