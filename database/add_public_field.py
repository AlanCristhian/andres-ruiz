from framework import servermodel


class AddPublicField:
    """Add a field called "public" to the *articles* table."""
    def __init__(self, database_bpath):
        self.collection = servermodel.Collection(dbpath=database_bpath)
        self.articles = self.collection.get('articles')

    def insert_public_field(self):
        self.collection.add_fields(name='articles', fields={'public': 'bool'})


if __name__ == '__main__':
    AddPublicField('database/models.db').insert_public_field()