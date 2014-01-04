import importlib
from framework import config


class MetaCollection(type):
    """Return a class to manage any database system."""
    def __new__(cls, name, bases, namespace, **kwds):
        """Return an child class of any of de DAL"""
        dbsystem=config.Config().databaseEngine
        # This set contains the database systems supported by this class
        implementedDatabases = {'sqlite3'}
        if dbsystem in implementedDatabases:
            # Import the module with the API methods for dbsystem
            try:
                databaseModule = importlib.import_module('framework.' + dbsystem + 'dal')
            except:
                raise ImportError('The module %s does not exist' % dbsystem)
        else:
            raise NotImplementedError("The %s database system does not implemented yet")
        extendedBases = bases + (databaseModule.Collection,)
        return super().__new__(cls, name, extendedBases, namespace, **kwds)


class Collection(metaclass=MetaCollection): pass