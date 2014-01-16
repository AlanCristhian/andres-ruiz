from framework import core


class UnittestHandler(metaclass=core.Main):

    def handler(self):
        self.templatePath = 'applications/specs/views/editarticle_test_template.html'
        self.basic_response(
            templatePath=self.templatePath,
            context={
                'title': 'Unittest',
                'salir': 'false',
            }
        )
