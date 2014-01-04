from framework import core
import os
import urllib.request
import copy
import uuid


class SaveImage(metaclass=core.Main):
    """Create all sizes of the images, save it and
    update the database with an generic path.
    """
    def get_buffer_image(self, form):
        """Obtain the raw image of the form"""
        if 'cid' in form:
            key = 'image_' + form.get('cid')
            return form.pop(key)
        else:
            keys = str(self.clientModel.form.keys())
            raise Exception(
                'The form object must have or "cid" fields' + keys)

    # I set the remove argument becaus I need a way to mocking the "remove"
    # method for the unittest.
    def setUp(self, remove=os.remove):
        self.currentDate = self.helpers.get_datetime()
        self.form = self.clientModel.form
        # Remember that the **id** field can be the article id or the image id
        self.idArticle = self.form.pop('id')
        self.rawImage = self.get_buffer_image(self.form)
        self.images = self.serverCollection.get('images')
        self.articles = self.serverCollection.get('articles')
        # articleData is an dictionary that contain all datas of the article
        # that call this handler.
        self.articleData = self.get_article()
        self.response.set_expires(0)
        self.remove = remove
        self.idImage = self.form.get('id_image')

    def get_article(self):
        return self.articles.get(
            fields='*'
            ,where='id=?'
            ,params=self.idArticle
            ,format='dictList')[0]

    def create_file_name(self):
        """I use the article name to create the name of each image."""
        # create a unique id for the file name
        index = self.helpers.alpha_uuid()
        return ( # concatenates the following data
            self.articleData.get('directory') +     # directory
            '/' +                                   # slash
            self.articleData.get('article_name') +  # the article name
            '-' +                                   # hyphen character
            index +                                 # the id of the image
            '.' + self.form.get('ext')              # extension
        )

    def save_file(self):
        newFilePath = self.create_file_name()
        oldFilePath = self.images.get(
            fields='url'
            ,where='id=?'
            ,params=self.idImage
            ,format='strList')
        # The row associate to the image data already exists in the
        # database becaus this row has been create previusly. So I use the
        # update operation.
        self.images.update(
            fields = {
                'last_modified': self.currentDate
                ,'url': newFilePath
            }
            ,where='id=?'
            ,params=self.idImage
        )
        with self.open(newFilePath, mode='wb') as imageFile:
            old = oldFilePath[0] if len(oldFilePath) else None
            try:
                self.remove(old)
            except:
                pass
            imageFile.write(self.rawImage)
        # Add the params because I need update this data in the single image
        # template.
        self.form.update(url=newFilePath)

    def handler(self):
        self.save_file()
        self.basic_response(
            content=self.form
            ,contentType='application/json')