import datetime
from framework import core


class SaveData(metaclass=core.Main):

    def setUp(self):
        self.articles = self.serverCollection.get('articles')
        self.model = self.clientModel.form
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
        self.basic_response(
            content={'status': True}
            ,contentType='application/json')