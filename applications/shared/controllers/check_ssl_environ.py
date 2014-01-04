from framework import core


class CheckSSLEnviron(metaclass=core.Main):

    def handler(self):
        self.basic_response(
            content=str(self.config.enableSharedSSL)
            ,contentType='text/plain')