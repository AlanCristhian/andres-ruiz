from framework import core


class ContactInfo(metaclass=core.Main):

    def setUp(self):
        self.contact = self.serverCollection.get('contact')
        self.data = self.contact.get(
            where='id=?'
            ,params='1'
            ,format='dictList')

    def handler(self):
        if self.data:
            self.basic_response(
                content=self.data[0]
                ,contentType='application/json')
        else:
            self.basic_response(
                content={}
                ,contentType='application/json')