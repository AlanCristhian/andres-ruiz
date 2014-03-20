import datetime
from framework import core


class SaveData(metaclass=core.Main):

    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.model = self.clientModel.form
        self.model.pop('FieldStorage')
        self.id = self.model.pop('id')
        self.response.set_expires(0)
        self.date = datetime.datetime.now()

    def handler(self):
        # set the modification date
        self.model.update({'last_modified': self.date})
        self.articles.update(
            fields=self.model
            ,where='id=?'
            ,params=self.id)
        self.model.pop('last_modified');
        self.basic_response(
            content=self.model
            ,contentType='application/json')