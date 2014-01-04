import unittest
import test
from applications.helpers import helpers


class ParagraphFilter(unittest.TestCase, test.CustomAssertions):

    def test_paragraph_filter(self):
        expectedValues = (
            ('a', '<p>a</p>')
            ,('\na', '<p>a</p>')
            ,('\r\r\na', '<p>a</p>')
            ,('a\n', '<p>a</p>')
            ,('a\n\r', '<p>a</p>')
            ,('\na\n', '<p>a</p>')
            ,('\ra', '<p>a</p>')
            ,('a\r', '<p>a</p>')
            ,('\ra\r', '<p>a</p>')
            ,('\na\r', '<p>a</p>')
            ,('\ra\n', '<p>a</p>')
            ,('a\nb', '<p>a</p><p>b</p>')
            ,('a\rb', '<p>a</p><p>b</p>')
            ,('a\n\nb', '<p>a</p><p>b</p>')
            ,('a\r\rb', '<p>a</p><p>b</p>')
            ,('a\n\rb', '<p>a</p><p>b</p>')
            ,('a\r\nb', '<p>a</p><p>b</p>')
        )
        for unformatText, expected in expectedValues:
            obtained = helpers.paragraph_filter(unformatText)
            self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()