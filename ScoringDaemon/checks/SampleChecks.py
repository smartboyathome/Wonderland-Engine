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
from datetime import datetime, timedelta

import time
from ScoringDaemon.check_types import ServiceCheck, InjectCheck

class SampleServiceCheck(ServiceCheck):
    def __init__(self, machine, team_id, db_host, db_port, db_name):
        super(SampleServiceCheck, self).__init__(machine, team_id, db_host, db_port, db_name)

    @property
    def timeout(self):
        return 15

    def run_check(self):
        self._mutable_vars.score = 5
        pass

class SampleInjectCheck(InjectCheck):
    def __init__(self, machine_id, team_id, db_host, db_port, db_name):
        super(SampleInjectCheck, self).__init__(machine_id, team_id, db_host, db_port, db_name)
        self._run_time = datetime.now() + timedelta(seconds=15)

    @property
    def timeout(self):
        return 15

    @property
    def time_to_run(self):
        return self._run_time

    @property
    def inject_number(self):
        return 0

    def run_check(self):
        self._mutable_vars.score = 5