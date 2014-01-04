import os
import sys
oldDirectory = os.getcwd()
os.chdir('..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from framework import servermodel
os.chdir(oldDirectory)


class Create_contact_info_Table:
    """Add the contact_info table, then get the data in contact table and set
    it in the contact_info table. Then associate it data to the andres_ruiz
    user. Finally drop the contact table."""
    pass


if __name__ == '__main__':
    database = Create_contact_info_Table()