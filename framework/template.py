"""This module contains a class with the method "render". This takes a
dictionary. This dictionary contains the path of a html template and
context.

The method "render" compiles the template with this context in a html
document. Then return the html document."""


from wheezy.template.ext.core import CoreExtension
from wheezy.template.ext.code import CodeExtension
from wheezy.template.engine import Engine
from wheezy.template.loader import FileLoader


class Render:
    """docstring for Render"""

    def render(self, result):
        """Take the function return value and renders a html document."""
        templateFile = result['templatePath']
        context = result['context']
       
        searchPath = ['']
        engine = Engine(
            loader=FileLoader(searchPath),
            extensions=[CoreExtension(), CodeExtension()])
        template = engine.get_template(templateFile)
        return template.render(context)