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
from configobj import ConfigObj
import pymongo, unittest, os
from ScoringServer import create_app

config_path = os.path.join(os.getcwd(), 'tests', 'testing.cfg')
create_app(config_path)
from ScoringServer import app

from tests.db_data import db_data

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db_name = app.config['DATABASE']['DB_NAME']
        self.db = pymongo.Connection()[db_name]
        if db_name in self.db.connection.database_names():
            #teardown wasn't run last time, so lets run it now.
            self.tearDown()
        self.data = db_data
        for key in self.data:
            mongodb_data = deepcopy(self.data[key])
            self.db[key].insert(mongodb_data)

    def tearDown(self):
        self.db.connection.drop_database(self.db.name)

    def get_team_data(self, team_id):
        result_data = deepcopy([i for i in self.data['teams'] if i['id'] == team_id][0])
        del result_data['id']
        return result_data

class DBTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigObj(config_path)['CORE']
        db_name = config['DATABASE']['DB_NAME']
        db_host = config['DATABASE']['HOST']
        db_port = config['DATABASE']['PORT']
        self.db = pymongo.Connection(db_host, db_port)[db_name]
        self.data = db_data
        for key in self.data:
            mongodb_data = deepcopy(self.data[key])
            self.db[key].insert(mongodb_data)
