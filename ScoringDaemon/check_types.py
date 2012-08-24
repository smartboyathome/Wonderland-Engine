'''
    Copyright (c) 2012 Alexander Abbott

    This file is part of the Cheshire Cyber Defense Scoring Engine (henceforth
    referred to as Cheshire).

    Cheshire is free software: you can redistribute it and/or modify it under
    the terms of the GNU Affero General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    Cheshire is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
    more details.

    You should have received a copy of the GNU Affero General Public License
    along with Cheshire.  If not, see <http://www.gnu.org/licenses/>.
'''

import abc
from DBWrappers.MongoDBWrapper import MongoDBWrapper

class Check(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def machine(self):
        '''
        The machine that the check will be run on.
        '''
        return

    @abc.abstractproperty
    def timeout(self):
        '''
        How long to wait for a result until the process is killed, in seconds.
        '''
        return

    @abc.abstractproperty
    def score(self):
        '''
        The score should be set to 0 before the check is run.
        '''
        return

    #@abc.abstractproperty
    #def check_type(self):
        #'''
        #The type of check as a string. These are mapped back to the DB.
        #'''
        #return

    @abc.abstractmethod
    def run_check(self):
        '''
        The check method itself.
        '''
        return

class ServiceCheck(Check):
    check_type = 'service'
    def __init__(self, machine_id, team_id, db_host, db_port, db_name):
        self.team_id = team_id
        self.db = MongoDBWrapper(db_host, db_port, db_name)
        self._score = 0
        self._machine_id = machine_id

    @property
    def machine(self):
        return self._machine_id

    @property
    def score(self):
        return self._score

    #@property
    #def check_type(self):
        #return 'service'

class InjectCheck(Check):
    check_type = 'inject'
    def __init__(self, machine_id, team_id, db_host, db_port, db_name):
        self.team_id = team_id
        self.db = MongoDBWrapper(db_host, db_port, db_name)
        self._score = 0
        self._machine_id = machine_id

    @property
    def score(self):
        return self._score

    @property
    def machine(self):
        return self._machine_id

    #@property
    #def check_type(self):
        #return 'inject'

    @abc.abstractproperty
    def time_to_run(self):
        '''
        The time at which this check will be run.
        '''
        return

    @abc.abstractproperty
    def inject_number(self):
        '''
        The number of the inject this is scoring.
        '''
        return

class AttackerCheck(Check):
    check_type = 'attacker'
    def __init__(self, machine_id, team_id, db_host, db_port, db_name):
        self.team_id = team_id
        self.db = MongoDBWrapper(db_host, db_port, db_name)
        self._score = 0
        self._machine_id = machine_id

    @property
    def score(self):
        return self._score

    @property
    def machine(self):
        return self._machine_id

    #@property
    #def check_type(self):
        #return 'attacker'