import datetime
import cgi
import os

import test
import unittest
from unittest.mock import Mock, PropertyMock
from applications.editArticle.controllers import save_multimedia_link


class SaveMultimediaLinkTest(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.save_multimedia_link = save_multimedia_link.SaveMultimediaLink(
            dependencies=test.mocks)
        '''
        self.FieldStorage = Mock(
            return_value={'id': 2, 'url': 'image/url', 'type': 'image_file'}
        )
        '''
        self.save_multimedia_link.get_article_model = Mock(return_value={})
        self.save_multimedia_link.handler()

    def test_SaveMultimediaLink_class(self):
        self.assertIsInstance(self.save_multimedia_link,
            save_multimedia_link.SaveMultimediaLink)

    def test_storage_property(self):
        self.assertHasAttr(self.save_multimedia_link, 'storage')

    def test_multimedia_collection_property(self):
        self.assertHasAttr(self.save_multimedia_link, 'multimedia_collection')

    def test_id_property(self):
        self.assertHasAttr(self.save_multimedia_link, 'id')

    def test_url_property(self):
        self.assertHasAttr(self.save_multimedia_link, 'url')

    def test_old_url_property(self):
        self.assertHasAttr(self.save_multimedia_link, 'old_url')

    def test_remove_method(self):
        self.assertHasAttr(self.save_multimedia_link, 'remove')


if __name__ == '__main__':
    unittest.main()
