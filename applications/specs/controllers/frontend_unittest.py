from framework import core


class UnittestHandler(metaclass=core.Main):

    def handler(self):
        self.templatePath = 'applications/specs/views/unittest.html'
        self.basic_response(
            templatePath=self.templatePath,
            context={
                'title': 'Unittest',
                'salir': 'false',
            }
        )
