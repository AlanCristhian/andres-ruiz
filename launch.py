#!/usr/bin/env python3.3
#!/home/andresru/dev/Python-3.3.0/python


import sys
import os
import cgitb


class Application:
    """Provide a web application that runs on Apache Server.

    Verify that your Hosting supports at least Python 3.3. Then place
    the content of this library in the "cgi-bin" folder.

    Config the application to import the libraries. Then compile the static
    files (.coffee and .less). Finaly route the application.
    """
    def __init__(self):
        # get config parameters
        from framework import config
        self.settings = config.Config()

    def main(self):
        """Set some things to work the framework.
        Then launch the application"""

        # Adds the current directory and path of the application
        sys.path.append(os.curdir)
        sys.path.append(os.path.join(os.curdir, "applications"))
        sys.path.append(os.path.join(os.curdir, "plugins"))
        sys.path.append(os.path.join(os.curdir, "framework"))

        # apply config parameters
        if not self.settings.consolelog:
            if self.settings.production:
                # Reports are saved in files within the folder app_logs
                cgitb.enable(
                    display=False
                    ,logdir=os.path.join(os.curdir, 'logs')
                    ,format='text')
            else:
                # the reports logs is displayed in the browser
                cgitb.enable()

        # Now I can import my framework libraries
        from framework import router
        try:
            from applications import handlers
        except:
            handlers = None
        router.Router(handlers, self.settings).route()


if __name__ == '__main__':
    app = Application()

    if app.settings.production:
        try:
            app.main()
        except Exception as e:
            import logging
            logFolder = os.path.join(os.curdir, "logs")
            logFolder = os.path.join(logFolder, "debug.log")
            logging.basicConfig(level=logging.DEBUG, filename=logFolder, filemode='w')
            logging.exception(str(e))
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Return an HTML document')
        parser.add_argument('--path', dest='url', help='An URL without protocol and server name.')
        arguments = parser.parse_args()
        if arguments.url:
            os.environ['PATH_INFO'] = arguments.url
        app.main()
