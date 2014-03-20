import cgi

from framework import core
from applications.helpers import helpers


class SetAsCover(metaclass=core.Main):
    def setUp(self, FieldStorage=cgi.FieldStorage):
        self.storage = FieldStorage()
        self.multimedia = self.serverCollection.get('multimedia')
        self.articles = self.serverCollection.get('articles')
        self.multimedia.update(
            fields={'cover': False},
            where='article_name=?',
            params=self.storage.getfirst('article_name'),
        )
        self.multimedia.update(
            fields={'cover': True},
            where='id=?',
            params=self.storage.getfirst('id'),
        )
        self.basic_response(
            content=self.multimedia.get(
                fields=('id', 'article_name'),
                where='cover=?',
                params=True,
            ),
            contentType='application/json',
        )