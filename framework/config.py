"""Provide a class tat generates global data to be used by the framework"""
import os
import itertools
from framework import helpers
from applications.settings import config


class Config(metaclass=helpers.Singleton):
    """Generates global data to be used by the framework"""
    def __init__(self):
        tuple(itertools.starmap(
            super().__setattr__
            ,config.items()
        ))
        self.serverName = os.environ.get('SERVER_NAME') or 'localhost'
        self.databasePath = self.databaseFolder + self.databaseFile
        self.protocol = helpers.get_protocol()