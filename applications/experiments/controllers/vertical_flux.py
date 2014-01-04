from framework import core


class VerticalFlux(metaclass=core.Main):
    """Experiment with an layout that flux
    from top to bottom and left to rigth.
    """
    def setUp(self):
        self.templatePath = 'applications/experiments/views/vertical_flux.html'

    def handler(self):
        self.unlogged_response(
            context={}
            ,templatePath=self.templatePath)