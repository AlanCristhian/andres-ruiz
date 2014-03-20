import datetime
from framework import core


class SaveMultimediaData(metaclass=core.Main):
    """Save or update new multimedia data. Also create the multimedia file.
    """
    def setUp(self):
        # Initialize all variables
        self.multimedia = self.serverCollection.get('multimedia')
        self.form = self.clientModel.form
        self.date = datetime.datetime.now()
        # config the response
        self.response.set_content_type('application/json')

    def create_new_multimedia(self):
        has_cover = self.multimedia.get(
            fields='id',
            where='article_name=? AND cover=?',
            params=(self.form.get('article_name'), True),
        )
        if has_cover:        
            self.multimedia.insert(
                article_name=self.form.get('article_name'),
                creation_date=self.date,
                cover=False)
        else:
            self.multimedia.insert(
                article_name=self.form.get('article_name'),
                creation_date=self.date,
                cover=True)

    def get_data_updates(self):
        """Get some fields of the last data inserted."""
        self.index = self.multimedia.lastModelIdChanged or self.form.get('id')
        if self.index:
            return self.multimedia.get(
                fields=('id', 'article_name', 'description', 'url', 'cover')
                ,where='id=?'
                ,params=self.index
                ,format='dictList'
            )[0]
        else:
            # if the value of the **self.index** var is None meaning that this is
            # the firs creation of the multimedia.
            return {'status': 'First insertion of the multimedia model.'}

    def update_multimedia_data(self):
        """Set the changes in the database."""
        self.multimedia.update(
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
            self.update_multimedia_data()
        else:
            self.create_new_multimedia()
        self.basic_response(content=self.get_data_updates())
