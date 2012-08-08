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
