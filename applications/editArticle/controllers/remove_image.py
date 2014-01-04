import os

from framework import core


class RemoveImage(metaclass=core.Main):
    """The app that hadle the article removal."""
    def setUp(self):
        if self.session.validate():
            self.response.set_content_type('application/json')
            self.form = self.clientModel.form;
            self.url = self.form.get('url')
            self.id = self.form.get('id')
            self.images = self.serverCollection.get('images')
            
    def remove(self, path):
        """Delete an entire directory tree. I set this alias to alow mocking.
        """
        return os.remove(path)

    def remove_image(self):
        self.images.remove(where='id=?', params=self.id)
        self.remove(self.url)

    def handler(self):
        if self.session.validate():
            self.remove_image()
            self.logged_response(content={'status': 'The image whas removed.'})
        else:
            self.logged_response(content={'status': 'you not permission.'})