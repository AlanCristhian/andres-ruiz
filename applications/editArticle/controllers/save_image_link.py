import datetime
import cgi
import os

from framework import core


class SaveImageLink(metaclass=core.Main):
    """Remove the old image if exists and store the new image link.
    """
    def handler(self, remove=os.remove, storage=None):
        self.remove = os.remove

        # Get client data
        if storage:
            # I set the storage argument for testing
            self.storage = storage
        else:
            self.storage = cgi.FieldStorage()

        self.id_image = self.storage.getfirst('id_image')
        self.url_image = self.storage.getfirst('url_image')
        self.type_image = self.storage.getfirst('type_image')

        # Get the images table
        self.image_collection = self.serverCollection.get('images')

        # Get the old image link
        self.old_url = self.image_collection.get(
            fields='url',
            where='id=?',
            params=self.id_image
        )

        # remove the old image if exists
        if len(self.old_url):
            try:
                self.remove(self.old_url[0])
            except (FileNotFoundError, TypeError):
                pass

        # update the new url
        self.image_collection.update(
                fields={
                    'last_modified': datetime.datetime.today(),
                    'url': self.url_image,
                },
                where='id=?',
                params=self.id_image,
            )

        # send a correct response
        self.basic_response(
            content='A new image link was updated: ' + repr(self.url_image),
            contentType='text/plain',
        )