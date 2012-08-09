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

from copy import deepcopy
import pymongo, unittest, os
from ScoringServer import create_app
from ScoringServer.utils import dict_to_mongodb_list

create_app(os.path.join(os.getcwd(), 'tests', 'testing.cfg'))
from ScoringServer import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db_name = app.config['DATABASE']['DB_NAME']
        self.db = pymongo.Connection()[db_name]
        if db_name in self.db.connection.database_names():
            #teardown wasn't run last time, so lets run it now.
            self.tearDown()
        self.data = {
            "teams": [
                {
                    "id": "1",
                    "name": "University of Washington, Seattle",
                    "score": 0
                },
                {
                    "id": "2",
                    "name": "Western Washington University",
                    "score": 0
                },
                {
                    "id": "6",
                    "name": "University of Washington, Bothell",
                    "score": 0
                }
            ]
        }
        for key in self.data:
            mongodb_data = deepcopy(self.data[key])
            self.db[key].insert(mongodb_data)

    def tearDown(self):
        self.db.connection.drop_database(self.db.name)

    def get_team_data(self, team_id):
        result_data = deepcopy([i for i in self.data['teams'] if i['id'] == team_id][0])
        del result_data['id']
        return result_data
