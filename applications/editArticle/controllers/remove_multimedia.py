import os

from framework import core


class RemoveMultimedia(metaclass=core.Main):
    """The app that hadle the article removal."""
    def setUp(self):
        if self.session.validate():
            self.response.set_content_type('application/json')
            self.form = self.clientModel.form;
            self.url = self.form.get('url')
            self.id = self.form.get('id')
            self.multimedia = self.serverCollection.get('multimedia')
            
    def remove(self, path):
        """Delete an entire directory tree. I set this alias to alow mocking.
        """
        try:
            os.remove(path)
        except (FileNotFoundError, TypeError):
            pass

    def remove_multimedia(self):
        self.multimedia.remove(where='id=?', params=self.id)
        self.remove(self.url)

    def handler(self):
        if self.session.validate():
            self.remove_multimedia()
            self.logged_response(content={'status': 'The multimedia whas removed.'})
        else:
            self.logged_response(content={'status': 'you not permission.'})