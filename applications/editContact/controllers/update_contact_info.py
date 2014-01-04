from framework import core


class UpdateInfo(metaclass=core.Main):

    def setUp(self):
        self.contact = self.serverCollection.get('contact')
        self.form = self.clientModel.form

    def handler(self):
        self.contact.update(
            fields={
                'address': self.form.get('address')
                ,'email': self.form.get('email')
                ,'facebook': self.form.get('facebook')
                ,'twitter': self.form.get('twitter')
                ,'pinterest': self.form.get('pinterest')
                ,'telephone': self.form.get('telephone')
                ,'mobile': self.form.get('mobile')}
            ,where='id=?'
            ,params='1')

    def tearDown(self):
        self.basic_response(
            content={'status': 'ok'}
            ,contentType='application/json'
            ,status=204)