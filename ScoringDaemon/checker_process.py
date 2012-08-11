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
from __future__ import division
from copy import deepcopy
from datetime import datetime, timedelta
from multiprocessing import Process, Event
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringDaemon.check_types import InjectCheck, ServiceCheck

class CheckerProcess(Process):
    def __init__(self, team_id, checks, db_host, db_port, db_name, check_delay):
        self.team_id = team_id
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.check_delay = check_delay
        super(CheckerProcess, self).__init__()
        self.shutdown_event = Event()
        self.checks = []
        for check_dict in checks:
            check_obj = check_dict['class'](team_id, db_host, db_port, db_name)
            if issubclass(check_dict['class'], InjectCheck):
                self.checks.append({
                    'id': check_dict['id'],
                    'object': check_obj,
                    'time_to_run': check_obj.time_to_run()
                })
            else:
                self.checks.append({
                    'id': check_id,
                    'object': check_obj,
                    'time_to_run': datetime.now()
                })

    def run(self):
        db = MongoDBWrapper(self.db_host, self.db_port, self.db_name)
        team = db.get_specific_team(self.team_id)
        while not self.shutdown_event.is_set():
            for check_dict in self.checks:
                check_obj = deepcopy(check_dict['object'])
                now = datetime.now()
                if check_dict['time_to_run'] < now:
                    check_process = Process(target=check_obj.run_check)
                    check_process.start()
                    check_process.join(check_obj.timeout)
                    if check_process.is_alive():
                        checker_process.terminate()
                    score = check_obj.score
                    if issubclass(type(check_obj), InjectCheck):
                        db.complete_inject_check(check_dict['id'], self.team_id, datetime.now(), score)
                        self.checks[:] = [obj for obj in self.checks if not obj == check_dict]
                    elif issubclass(type(check_obj), ServiceCheck):
                        db.complete_service_check(check_dict['id'], self.team_id, datetime.now(), score)
                        check_dict['timestamp'] = datetime.now() + timedelta(seconds=self.check_delay)
                    else: # it is an attacker check
                        db.complete_attacker_check(check_dict['id'], self.team_id, datetime.now(), score)
                        check_dict['timestamp'] = datetime.now() + timedelta(seconds=self.check_delay)
                if self.shutdown_event.is_set():
                    break