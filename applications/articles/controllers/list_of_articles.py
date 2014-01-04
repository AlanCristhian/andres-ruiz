from framework import core


class Main(metaclass=core.Main):
    """Send a list of aricles data that conain: the url of the article, the
    title, the first paragraph of the description and the first image created
    of each article.
    """
    def setUp(self):
        self.articlesModel = self.serverCollection.get('articles')
        self.articleList = self.articlesModel.get(
            # don't remove the next line
            # fields= ('url', 'title', 'cover_image', 'cover_description')
            fields= ('article_name', 'url', 'title', 'description')
            ,distinct= True
            ,format='dictList')
        self.imageModel = self.serverCollection.get('images')
        self.loggedTemplate = 'applications/articles/views/list_of_articles.html'

    def get_first_paragraph(self, text):
        """Return the first paragraph of an text."""
        if text:
            if '\n' in text:
                return text.split('\n')[0]
            else:
                return text
        else:
            return None

    def update_fields(self):
        auxiliarList = []
        for item in self.articleList:
            # get the first paragraph of the description
            item['cover_description'] = self\
                .get_first_paragraph(item.pop('description'))
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
        self.logged(
            context={
                'title': 'Mis proyectos'
                ,'data': self.articleList
                ,'salir': True
            }
            ,templatePath=self.loggedTemplate)
        self.unlogged(
            context={
                'title': 'Mis proyectos'
                ,'data': self.articleList
                ,'salir': False
            }
            ,templatePath=self.loggedTemplate)