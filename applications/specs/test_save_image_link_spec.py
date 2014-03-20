import datetime
import cgi
import os

import test
import unittest
from unittest.mock import Mock, PropertyMock
from applications.editArticle.controllers import save_image_link


class SaveImageLinkTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.save_image_link = save_image_link.SaveImageLink(
            dependencies=test.mocks)
        storage = cgi.FieldStorage()
        self.save_image_link.get_article_model = Mock(return_value={})
        self.save_image_link.handler(os.remove, storage)

    def test_SaveImageLink_class(self):
        self.assertIsInstance(self.save_image_link,
            save_image_link.SaveImageLink)

    def test_storage_property(self):
        self.assertHasAttr(self.save_image_link, 'storage')

    def test_image_collection_property(self):
        self.assertHasAttr(self.save_image_link, 'image_collection')

    def test_id_image_property(self):
        self.assertHasAttr(self.save_image_link, 'id_image')

    def test_url_image_property(self):
        self.assertHasAttr(self.save_image_link, 'url_image')

    def test_old_url_property(self):
        self.assertHasAttr(self.save_image_link, 'old_url')

    def test_remove_method(self):
        self.assertHasAttr(self.save_image_link, 'remove')


if __name__ == '__main__':
    unittest.main()
