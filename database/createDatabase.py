import os
import sys
oldDirectory = os.getcwd()
os.chdir('..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')

from framework import servermodel
os.chdir(oldDirectory)

class DataModel:
    """Create all tables and triggers into the database."""
    def __init__(self):
        self.collection = servermodel.Collection(
            dbpath='models.db')
        # article models
        self.collection.create(name='articles', fields={
            'id':                   'intPrim'
            ,'title':               'str'
            ,'classification':      'str'
            ,'url':                 'str'
            ,'edit_url':            'str'
            ,'country':             'str'
            ,'state':               'str'
            ,'city':                'str'
            ,'autor':               'str'
            ,'colaborators':        'str'
            ,'project_date':        'str'
            ,'creation_date':       'datetime'
            ,'last_modified':       'datetime'
            ,'description':         'str'
            ,'cover_image':         'str'
            ,'cover_description':   'str'
            ,'article_name':        'str'
            ,'directory':           'str'
            ,'acceptance':          'float'
            ,'views':               'int'
            ,'likes':               'int'
            ,'dislikes':            'int'
        })
        self.collection.create(name='images', fields={
            'id':               'intPrim'
            ,'creation_date':   'datetime'
            ,'last_modified':   'datetime'
            ,'url':             'str'
            ,'description':     'str'
            ,'classification':  'str'
            ,'article_name':    'str'
            ,'position':        'int'
            ,'acceptance':      'float'
            ,'zoomed':          'int'
            ,'likes':           'int'
            ,'dislikes':        'int'
        })
        self.collection.create(name='videos', fields={
            'id':               'intPrim'
            ,'creation_date':   'datetime'
            ,'last_modified':   'datetime'
            ,'url':             'str'
            ,'description':     'str'
            ,'classification':  'str'
            ,'position':        'int'
            ,'article_name':    'str'
        })

        self.collection.create(name='comments', fields={
            'id':               'intPrim'
            ,'creation_date':   'datetime'
            ,'last_modified':   'datetime'
            ,'url':             'str'
            ,'user_name':       'str'
            ,'content':         'str'
            ,'likes':           'int'
            ,'dislikes':        'int'
            ,'spam':            'bool'
            ,'inappropriate':   'bool'
            ,'article_name':    'str'
        })

        self.collection.create(name='visitors', fields={
            'id':               'intPrim'
            ,'creation_date':   'datetime'
            ,'last_modified':   'datetime'
            ,'user_name':       'str'
            ,'email':           'str'
            ,'banned':          'bool'
            ,'banned_date':     'datetime'
            ,'id_visitor':      'int'
        })

        self.collection.bind(
            bindName='images_to_articles'
            ,modelSource='images'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name'
        )
        self.collection.bind(
            bindName='videos_to_articles'
            ,modelSource='videos'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name'
        )
        self.collection.bind(
            bindName='comments_to_articles'
            ,modelSource='comments'
            ,fieldSource='article_name'
            ,modelTarget='articles'
            ,fieldTarget='article_name'
        )
        self.collection.bind(
            bindName='visitors_to_comments'
            ,modelSource='visitors'
            ,fieldSource='id_visitor'
            ,modelTarget='comments'
            ,fieldTarget='id'
        )
        # admin models
        self.collection.create(name='users', fields={
            'id':           'intPrim'
            ,'user_name':  'str'
            ,'password':    'str'
        })
        self.collection.create(name='contact', fields={
            'id':           'intPrim'
            ,'user_name':   'str'
            ,'address':     'str'
            ,'email':       'str'
            ,'facebook':    'str'
            ,'twitter':     'str'
            ,'pinterest':   'str'
            ,'telephone':   'str'
            ,'mobile':      'str'
        })
        self.collection.create(name='sessions', fields={
            'id':            'prim',
            'data':          'str',
            'created_time':  'datetime',
            'accessed_time': 'datetime',
            'expire_time':   'datetime',
            'remote_addr':   'str'
        })

        # location models
        self.collection.create(name='location', fields={
            'id':               'intPrim'
            ,'country_name':    'str'
            ,'state_name':      'str'
            ,'city_name':       'str'
            ,'created_at':      'str'
        })

    def create_loaction(self):
        """Set initial values to save all scheme."""
        locationModel = self.collection.get('location')
        # set the location data
        with open('location.txt') as locationFile:
            line = locationFile.readline()
            fixLine = line.replace("'", "")
            row = tuple(fixLine.split(','))
            while line != '':
                locationModel.insert(
                    country_name=row[0]
                    ,state_name=row[1]
                    ,city_name=row[2]
                    ,created_at=row[3])
                line = locationFile.readline()
                fixLine = line.replace("'", "")
                row = tuple(fixLine.split(','))
        # make a void "contact" table
        self.collection.get('contact').insert(
            user_name=''
            ,address=''
            ,email=''
            ,facebook=''
            ,twitter=''
            ,pinterest=''
            ,telephone=''
            ,mobile=''
        )


if __name__ == '__main__':
    database = DataModel()
    database.create_loaction()