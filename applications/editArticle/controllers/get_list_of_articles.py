from framework import core


class ListOfArticles(metaclass=core.Main):
    """Response a list of articles."""
    def setUp(self):
        self.articleModel = self.serverCollection.get('articles')
        self.articleList = self.articleModel.get(
            fields=('id', 'title', 'edit_url', 'article_name')
            ,format='dictList'
        )
        self.imageModel = self.serverCollection.get('images')

    def get_first_paragraph(self, text):
        """Return the first paragraph of an text."""
        if '\n' in text:
            return text.split('\n')[0]
        else:
            return text

    def update_fields(self):
        auxiliarList = []
        for item in self.articleList:
            # Get the url of the first image uploaded. The sqlite3 database
            # engine return the ascendent order by default.
            try:
                url = self.imageModel.get(
                    fields='url'
                    ,where='article_name=?'
                    ,params=item['article_name']
                    ,format='strList'
                )[0]
            except:
                url = ''
            item['cover_image'] = url
            auxiliarList = auxiliarList + [item]
        # update all fields
        self.articleList = auxiliarList


    def handler(self):
        self.update_fields()
        self.logged_response(
            content=self.articleList
            ,contentType='application/json'
        )