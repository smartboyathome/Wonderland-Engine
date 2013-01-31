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
from datetime import datetime
import json
import unittest
from CheshireCat import create_app
from tests import DBTestCaseMixin, config_path
create_app(config_path)
from CheshireCat import app

class FlaskTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        self.app = app.test_client()
        db_host = app.config['DATABASE']['HOST']
        db_port = app.config['DATABASE']['PORT']
        db_name = app.config['DATABASE']['DB_NAME']
        self.init_db_data(db_host, db_port, db_name)

    def tearDown(self):
        self.drop_db_data()

    def get_team_data(self, team_id):
        result_data = deepcopy([i for i in self.data['teams'] if i['id'] == team_id][0])
        del result_data['id']
        return result_data

    def login_user(self, username, password):
        query_data = {
            'username': username,
            'password': password
        }
        return self.app.post('/session', data=json.dumps(query_data))

    def logout_user(self):
        self.app.delete('/session')