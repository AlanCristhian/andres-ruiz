import unittest
import test
from unittest.mock import Mock
from applications.editArticle.controllers import get_article_data


class GetArticleComponents(unittest.TestCase, test.CustomAssertions):

    def setUp(self):
        self.getData = get_article_data.GetData(dependencies=test.mocks)
        self.getData.basic_response = Mock()
        self.getData.warnings = False

    def test_should_has_an_GetArticle_instance(self):
        self.assertIsInstance(self.getData, get_article_data.GetData)

    def test_should_get_article_info(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.get_article_info = Mock(return_value=None)
        self.getData.handler()
        self.assertCalled(self.getData.get_article_info)

    def test_should_return_a_void_response_if_no_articleURL(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.handler()
        self.getData.basic_response.assert_called_with(content={})

    def test_should_return_a_void_response_if_no_article_content(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.get_article_info = Mock(return_value=[])
        self.getData.handler()
        self.getData.basic_response.assert_called_with(content={})

    def test_should_return_the_article_info(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.get_article_info = Mock(return_value=[{'any': 'data'}])
        self.getData.handler()
        self.getData.basic_response.assert_called_with(content={'any': 'data'})

    def test_should_get_article_description(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'description'}
        self.getData.get_article_description = Mock(return_value=[
            {'description': 'any text'}])
        self.getData.handler()
        self.getData.basic_response.assert_called_with(
            content={'description': 'any text'})

    def test_should_call_get_data_method(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.get_data = Mock()
        self.getData.handler()
        self.assertCalled(self.getData.get_data)

    def test_should_get_article_cover(self):
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'cover'}
        self.getData.get_article_cover = Mock()
        self.getData.handler()
        self.assertCalled(self.getData.basic_response)

    def test_get_article_multimedia(self):
        self.getData.articleName = [0]
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'multimedia'}
        self.getData.get_article_multimedia = Mock(
            return_value=[{'any': 'data'}])
        self.getData.handler()
        self.assertCalled(self.getData.basic_response)

    def test_expiration_date(self):
        """The expiration date should be cero."""
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.handler()
        self.getData.response.set_expires.assert_called_with(0)

    def test_content_type(self):
        """The content type should be json."""
        self.getData.clientModel.form = {
            'edit_url': '/any/url'
            ,'data_group': 'info'}
        self.getData.handler()
        self.getData.response.set_content_type\
            .assert_called_with('application/json')


if __name__ == '__main__':
    unittest.main()