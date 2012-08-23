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
import json
from multiprocessing.process import Process
from configobj import ConfigObj
import pymongo, unittest, os
import redis
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringDaemon.master import Master
from ScoringServer import create_app

config_path = os.path.join(os.getcwd(), 'testing.cfg')
create_app(config_path)
from ScoringServer import app

from tests.db_data import db_data

class DBTestCaseMixin(object):
    def init_db_data(self, db_host, db_port, db_name):
        self.db = pymongo.Connection(db_host, int(db_port), safe=True)[db_name]
        if db_name in self.db.connection.database_names():
            #teardown wasn't run last time, so lets run it now.
            self.drop_db_data()
        self.data = deepcopy(db_data)
        for key in self.data:
            mongodb_data = deepcopy(self.data[key])
            self.db[key].insert(mongodb_data)

    def drop_db_data(self):
        self.db.connection.drop_database(self.db.name)

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

class DBTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        config = ConfigObj(config_path)['CORE']
        db_host = config['DATABASE']['HOST']
        db_port = config['DATABASE']['PORT']
        db_name = config['DATABASE']['DB_NAME']
        self.init_db_data(db_host, db_port, db_name)
        self.db_wrapper = MongoDBWrapper(db_host, int(db_port), db_name)

    def tearDown(self):
        self.drop_db_data()

class DaemonTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        config = ConfigObj(config_path)['CORE']
        db_host = config['DATABASE']['HOST']
        db_port = config['DATABASE']['PORT']
        db_name = config['DATABASE']['DB_NAME']
        self.init_db_data(db_host, db_port, db_name)
        self.redis = redis.Redis(config['REDIS']['HOST'], int(config['REDIS']['PORT']), password=config['REDIS']['PASSWORD'])
        self.daemon_channel = config['REDIS']['DAEMON_CHANNEL']
        self.master = Master(config_path)
        self.master_process = Process(target=self.master.run)
        self.master_process.start()

    def tearDown(self):
        self.redis.publish(self.daemon_channel, 'shutdown')
        if self.master_process.is_alive():
            self.master_process.join(5)
            if self.master_process.is_alive():
                self.master_process.terminate()
        self.drop_db_data()