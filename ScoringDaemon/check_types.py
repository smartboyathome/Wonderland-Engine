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

    @abc.abstractmethod
    def score(self):
        '''
        The score for the check. If this is a ServiceCheck, then it will return the score to be added each time.
        '''
        return

    @abc.abstractmethod
    def run_check(self):
        '''
        The check method itself.
        '''
        return

class ServiceCheck(Check):
    pass

class InjectCheck(Check):
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

class ManualCheck(Check):
    def __init__(self, machine, timeout, inject_number, comments, score):
        self._machine = machine
        self._timeout = timeout
        self._comments = comments
        self._inject_number = inject_number
        self._score = score

    @property
    def machine(self):
        return self._machine

    @property
    def timeout(self):
        return self._timeout

    def run_check(self):
        return True

    @property
    def inject_number(self):
        return self._inject_number

    @property
    def comments(self):
        return self._comments

    @property
    def score(self):
        return self._score

class AttackerCheck(Check):
    pass