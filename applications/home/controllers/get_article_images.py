from framework import core


class GetArticleModel(metaclass=core.Main):
    """Response a JSON with all info of the article.
    """
    def setUp(self):
        self.article = self.serverCollection.get('articles')
        self.images = self.serverCollection.get('images')
        self.get_article_name()


    def get_article_name(self):
        """Return the name of the article binded to the actual url.
        """
        # get the article url
        if hasattr(self.clientModel, 'https') \
        and self.config.enableSharedSSL:
            self.article_URL = self.clientModel.url.replace('/~andresru/images/', '')
        else:
            self.article_URL = self.clientModel.url.replace('/images/', '')

        # get fields
        return self.article.get(
            fields='article_name'
            ,where='url=?'
            ,params=self.article_URL
            ,distinct=True)

    def get_images(self, url=None):
        """Return a list with image info.
        """
        return self.images.get(
            fields=('id', 'url', 'article_name', 'description')
            ,where='article_name=?'
            ,params=url
            ,format='dictList')

    def handler(self):
        _article_name = self.get_article_name()
        if _article_name:
            _content = self.get_images(_article_name[0][0])
            self.basic_response(
                content=_content,
                contentType='application/json',
            )
        else:
            self.basic_response(
                content={'error': self.article_URL + ' not exists'},
                contentType='application/json',
            )