import shutil
import os

from framework import servermodel

# TODO:
# - Remove the images table.
# - Remove the videos table.
# - Remove the location table.

# Create a copy of models.db
shutil.copyfile('database/models.db', 'models_copy.db')
shutil.copystat('database/models.db', 'models_copy.db')


class AddMissingData:
    def __init__(self):
        assert os.path.lexists('models_copy.db'), \
            'you must create a copy of models.db called models_copy.db'
        self.collection = servermodel.Collection(dbpath='models_copy.db');

    def __enter__(self): 
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def add_contact_info_table(self):
        """Create the *contact_info* table."""
        self.collection.create(name='contact_info', fields={
            'id':              'intPrim',
            'service_name':    'str',
            'service_address': 'str',
            'user_name':       'str',
            'data':            'str',
        })
        self.collection.bind(
            bindName='contact_info_to_users',
            modelSource='contact_info',
            fieldSource='user_name',
            modelTarget='users',
            fieldTarget='user_name',
        )

        # get the contact_info table
        self.contact_info = self.collection.get('contact_info')
        self.contact = self.collection.get('contact')

    def insert_contact_info_data(self):
        # Get the user_name register.
        try:
            _users = self.contact.get(
                fields='user_name',
                format='strList',
            )
        except IndexError as e:
            raise e

        for _user_name in _users:
            # Set the address register
            try:
                _address = self.contact.get(
                    fields='address',
                    where='user_name=?',
                    params=_user_name,
                    format='strList',
                )[0]
            except IndexError:
                _address = None
            finally:
                if _address and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='address',
                        service_address=_address,
                    )

            # Set the email register
            try:
                _email = self.contact.get(
                    fields='email',
                    format='strList',
                )[0]
            except IndexError:
                _email = None
            finally:
                if _email and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='email',
                        service_address=_email,
                    )

            # Set the facebook register.
            try:
                _facebook = self.contact.get(
                    fields='facebook',
                    format='strList',
                )[0]
            except IndexError:
                _facebook = None
            finally:
                if _facebook and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='facebook',
                        service_address=_facebook,
                    )

            # Set the twitter register.
            try:
                _twitter = self.contact.get(
                    fields='twitter',
                    format='strList'
                )[0]
            except IndexError:
                _twitter = None
            finally:
                if _twitter and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='twitter',
                        service_address=_twitter,
                    )

            # Set the pinterest register.
            try:
                _pinterest = self.contact.get(
                    fields='pinterest',
                    format='strList',
                )[0]
            except IndexError:
                _pinterest = None
            finally:
                if _pinterest and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='pinterest',
                        service_address=_pinterest,
                    )

            # Set the telephone register
            try:
                _telephone = self.contact.get(
                    fields='telephone',
                    format='strList',
                )[0]
            except IndexError:
                _telephone = None
            finally:
                if _telephone and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='telephone',
                        service_address=_telephone,
                    )

            # Set the mobile register.
            try:
                _mobile = self.contact.get(
                    fields='mobile',
                    format='strList'
                )[0]
            except:
                _mobile = None
            finally:
                if _mobile and _address != 'None':
                    self.contact_info.insert(
                        user_name=_user_name,
                        service_name='mobile',
                        service_address=_mobile,
                    )

    def add_multimedia_table(self):
        """Create the *multimedia* table."""
        self.collection.create(name='multimedia', fields={
            'id':              'intPrim',
            'creation_date':   'datetime',
            'last_modified':   'datetime',
            'url':             'str',
            'description':     'str',
            'classification':  'str',
            'article_name':    'str',
            'position':        'int',
            'acceptance':      'float',
            'zoomed':          'int',
            'likes':           'int',
            'dislikes':        'int',
            'data':            'str',
            'cover':           'bool',
            'type':            'str',
        })
        self.collection.bind(
            bindName='multimedia_to_articles',
            modelSource='multimedia',
            fieldSource='article_name',
            modelTarget='articles',
            fieldTarget='article_name',
        )
        self.multimedia = self.collection.get('multimedia')
        self.images = self.collection.get('images')

    def add_multimedia_data(self):
        _images = self.images.get(
            fields='*',
            format='dictList'
        )
        for _image in _images:
            _multimedia = _image
            _multimedia.update({'type': 'image_file'})
            self.multimedia.insert(**_multimedia)

    def add_missing_fields(self):
        _fields = {'data': 'str'}
        self.collection.add_fields(name='articles', fields=_fields)
        self.collection.add_fields(name='comments', fields=_fields)
        self.collection.add_fields(name='visitors', fields=_fields)
        self.collection.add_fields(name='users', fields=_fields)

    def remove_tables(self):
        self.collection.remove(name='images')
        self.collection.remove(name='videos')
        self.collection.remove(name='location')
        self.collection.remove('images_to_articles')
        self.collection.remove('videos_to_articles')
        #self.collection.remove(name='contact')


if __name__ == '__main__':
    with AddMissingData() as _:
        _.add_contact_info_table()
        _.insert_contact_info_data()
        _.add_multimedia_table()
        _.add_multimedia_data()
        _.add_missing_fields()
        #_.remove_tables()