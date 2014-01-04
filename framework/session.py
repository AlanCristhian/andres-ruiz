import datetime
import os
import random
import hashlib
import sys

from framework import servermodel
from framework import helpers
from framework import config
from framework import clientModel


class Session:
    def __init__(self
        ,servermodelDependence=servermodel.Collection(dbpath=config.Config().databasePath)
        ,configDependence=config.Config()
        ,helpersDependence=helpers
        ,clientModelDependence=clientModel.Model()
    ):
        self.servermodel = servermodelDependence
        self.config = configDependence
        self.helpers = helpersDependence
        self.clientModel = clientModelDependence
        self.model = self._get_sessions_model()
        # remove expired sessions
        self.model.remove(
            where="expire_time < ?",
            params=helpers.get_datetime()
        )
        self.clientID = self._get_client_id()

    def validate(self):
        # has cookie in client
        if self.clientID:
            self.serverData = self.model.get(
                fields='id'
                ,where='id=?'
                ,params=self.clientID
                ,format='dictList'
                ,distinct=True
            )
            # the client cookie value and server id value are equal
            if self.serverData:
                self.serverID = self.serverData[0]['id']
                self.data = self._get_session_data(self.serverID)
                # self._update_session(self.serverID)
                return True
            # the client cookie value is not equal to the server id value
            else:
                return False
        # no cookie in client
        else:
            return False

    def create(self):
        self.newSessionId = self._create_new_id()
        self.model.insert(
            id=self.newSessionId
            ,created_time=helpers.get_datetime()
            ,accessed_time=helpers.get_datetime()
            ,expire_time=helpers.get_datetime(self.get_max_age())
            ,remote_addr=self.clientModel.ip
        )

    def remove(self):
        self.model.remove(
            where="id=?",
            params=self._get_client_id()
        )

    def get_cookie_value(self):
        return self.newSessionId

    def _create_new_id(self):
        """create a new and unique session id"""
        while True:
            now = datetime.datetime.today()
            seed = '%s%s%s' % (str(os.getpid()),
                                str(now.isoformat()),
                                str(random.randint(0, sys.maxsize - 1)))
            message = hashlib.new('sha256')
            message.update(seed.encode('utf-8'))
            newID = message.hexdigest()
            foundID = self.model.get(
                fields='id',
                where='id=?',
                params=newID
            )
            if not foundID:
                return newID

    def _get_sessions_model(self):
        """return a model of sessions table.
        Create sessions table not exists."""
        if not self.servermodel.has('sessions'):
            self.servermodel.create(
                name='sessions',
                fields={
                    'id':            'prim'
                    ,'data':          'str'
                    ,'created_time':  'datetime'
                    ,'accessed_time': 'datetime'
                    ,'expire_time':   'datetime'
                    ,'remote_addr':   'str'
                }
            )
        return self.servermodel.get('sessions')

    def _get_client_id(self):
        # Get the current cookie session
        cookie = self.clientModel.cookie
        # get the cookie value
        if self.config.cookieName in cookie:
            return cookie[self.config.cookieName].value
        else:
            return None

    def _get_session_data(self, serverID):
        return self.model.get(
            fields='*'
            ,where='id=?'
            ,params=serverID
            ,format='dictList'
        )[0]

    def get_max_age(self):
        """Returns the number of seconds the session live"""
        timeSession = self.config.timeSession.split(' ')
        time = int(timeSession[0])
        unity = timeSession[1]
        delta = {
            'minutes': lambda t: t * 60
            ,'hours': lambda t: t * 3600
            ,'days': lambda t: t * 86400
            ,'weeks': lambda t: t * 604800
            ,'months': lambda t: t * 2419200
            ,'years': lambda t: t * 31536000
        }
        return delta[unity](time)
