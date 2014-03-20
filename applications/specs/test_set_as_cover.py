import cgi
import unittest
import test
from unittest.mock import Mock

from applications.editArticle.controllers import set_as_cover

class SetAsCoverTest(unittest.TestCase, test.CustomAssertions):
    def setUp(self):
        self.set_as_cover = set_as_cover.SetAsCover(dependencies=test.mocks,
            warnings=False)
        self.FieldStorage = cgi.FieldStorage
        self.FieldStorage.getfirst = Mock(return_value="/article/name")
        self.set_as_cover.setUp(self.FieldStorage)

    def test_SetAsCover_class(self):
        self.assertIsInstance(self.set_as_cover, set_as_cover.SetAsCover)

    def test_storage_property(self):
        self.assertHasAttr(self.set_as_cover, 'storage')

    def test_multimedia_property(self):
        self.assertHasAttr(self.set_as_cover, 'multimedia')

    def test_articles_property(self):
        self.assertHasAttr(self.set_as_cover, 'articles')


if __name__ == '__main__':
    unittest.main()