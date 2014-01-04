import os
import sys
import unittest


# change directroy for import my libraries
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')
from framework import helpers

print(helpers.get_datetime())
print(helpers.get_datetime(3600))