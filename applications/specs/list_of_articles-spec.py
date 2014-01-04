import unittest
import test
from applications.articles.controllers import list_of_articles as articles


class AdminCompents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.articles = articles.Main(dependencies=test.mocks)
        self.articles.setUp()
        self.articles.handler()

    def test_isinstance_of_main(self):
        self.assertIsInstance(self.articles, articles.Main)

    def test_get_list_of_articles(self):
        self.articles.articlesModel.get.assert_called_with(
            # don't remove the next line
            # fields= ('url', 'title', 'cover_image', 'cover_description')
            fields= ('article_name', 'url', 'title', 'description')
            ,distinct= True
            ,format='dictList'
        )

    def test_logged_template(self):
        self.assertFileExists(self.articles.loggedTemplate)

    def test_split_description(self):
        """Should get the first paragrap."""
        obtained = self.articles.get_first_paragraph('a\nb')
        expected = 'a'
        self.assertEqual(obtained, expected)

    @unittest.expectedFailure
    def test_cover_image_path(self):
        """should make the cover image path."""
        raise AssertionError

    @unittest.expectedFailure
    def test_cover_description(self):
        """should make the cover description."""
        raise AssertionError


if __name__ == '__main__':
    unittest.main()
