import datetime
from framework import core


class SaveImageData(metaclass=core.Main):
    """Save or update new image data. Also create the image file.
    """
    def setUp(self):
        # Initialize all variables
        self.images = self.serverCollection.get('images')
        self.form = self.clientModel.form
        self.date = datetime.datetime.now()
        # config the response
        self.response.set_content_type('application/json')

    def create_new_image(self):
        self.images.insert(article_name=self.form.get('article_name'))
        self.images.update(
            fields={
                'creation_date': self.helpers.get_datetime()
            }
            ,where='id=?'
            ,params=self.images.lastModelIdChanged
        )

    def get_data_updates(self):
        """Get some fields of the last data inserted."""
        self.index = self.images.lastModelIdChanged or self.form.get('id')
        if self.index:
            return self.images.get(
                fields=('id', 'article_name', 'description', 'url')
                ,where='id=?'
                ,params=self.index
                ,format='dictList'
            )[0]
        else:
            # if the value of the **self.index** var is None meaning that this is
            # the firs creation of the image.
            return {'status': 'First insertion of the image model.'}

    def update_image_data(self):
        """Set the changes in the database."""
        self.images.update(
            fields={
                'description': self.form.get('description')
                ,'url': self.form.get('url')
                # set the modification date
                ,'last_modified': self.date
            }
            ,where='id=?'
            ,params=self.form.get('id')
        )

    def handler(self):
        if self.form.get('id'):
            self.update_image_data()
        else:
            self.create_new_image()
        self.basic_response(content=self.get_data_updates())
