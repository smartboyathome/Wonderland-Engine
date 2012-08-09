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

from multiprocessing import Process
from DBWrappers.MongoDBWrapper import MongoDBWrapper

class CheckerProcess(Process):
    def __init__(self, team_id, checks, db_host, db_port, db_name):
        self.team_id = team_id
        self.checks = checks
        self.db_host, self.db_port, self.db_name = db_host, db_port, db_name
    def run(self, queue):
        db = MongoDBWrapper(self.db_host, self.db_port, self.db_name)
        team = db.get_specific_team(self.team_id)

        for command in queue:
            if command == 'quit':
                db.close()
                return