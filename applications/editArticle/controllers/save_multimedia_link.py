import datetime
import cgi
import os

from framework import core


class SaveMultimediaLink(metaclass=core.Main):
    """Store the new multimedia link. Also remove the old image file if exists.
    """
    def handler(self, remove=os.remove, FieldStorage=cgi.FieldStorage):
        self.remove = os.remove

        # Get client data
        self.storage = FieldStorage()

        self.id = self.storage.getfirst('id')
        self.url = self.storage.getfirst('url')
        self.type = self.storage.getfirst('type')

        # Get the multimedia table
        self.multimedia_collection = self.serverCollection.get('multimedia')

        # Get the old image link
        self.old_url = self.multimedia_collection.get(
            fields='url',
            where='id=?',
            params=self.id,
            format='strList',
        )

        # remove the old image if exists
        if len(self.old_url):
            try:
                self.remove(self.old_url[0])
            except FileNotFoundError:
                pass

        # update the new url
        self.multimedia_collection.update(
                fields={
                    'last_modified': datetime.datetime.today(),
                    'url': self.url,
                    'type': self.type,
                },
                where='id=?',
                params=self.id,
            )

        # send a correct response
        self.basic_response(
            content={
                'updated': True,
                'url': repr(self.url),
                'type': repr(self.type),
            },
            contentType='application/json',
        )