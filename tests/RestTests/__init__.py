from copy import deepcopy
from datetime import datetime
import json
import unittest
from ScoringServer import app
from tests import DBTestCaseMixin

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
        return self.app.post('/session/', data=json.dumps(query_data))

    def logout_user(self):
        self.app.delete('/session/')