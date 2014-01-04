"""This library involves common tasks for testing"""


import os
import sys


class Test:
    """This class is based on boilerplate.py library
    into specs folder. This runs the common settings to
    test the libraries within the Applications folder.
    """
    def __init__(self, directory='root'):
        # remember the original directory
        oldDirectory = os.getcwd()
        # change to directory root
        os.chdir('../..')
        # remember the path of directory root
        rootDirectory = os.getcwd()
        # add root, framework an aplications direcories to sys
        sys.path.append(rootDirectory)
        sys.path.append(rootDirectory + '/framework')
        sys.path.append(rootDirectory + '/plugins')
        sys.path.append(rootDirectory + '/applications')
        if directory is 'root':
            # maintain into root directory
            # self.directory = rootDirectory
            pass
        elif directory is 'current':
            # come back to original directory where place the test
            os.chdir(oldDirectory)
            # self.directory = oldDirectory
        else:
            raise ValueError(
                'the "directory" argument can must be "roor" or "current".')
        self.directory = directory

        from framework import dependencies
        self.mocks = dependencies.mocks
        self.dependencies = dependencies

        from framework import test
        self.CustomAssertions = test.CustomAssertions


def extends(source, destination):
    """Copy the properties of an source
    object into another destination object."""
    properties = dir(source)
    for i in properties:
        # Don't copy operator methods. Neither copy existing methods.
        # if (not '__' in i) and (not i in dir(destination)):
        if not '__' in i:
            try:
                destination[i] = source.__getattribute__(i)
            except:
                destination.__setattr__(i, source.__getattribute__(i))


extends(Test(), globals())
