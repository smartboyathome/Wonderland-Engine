import unittest
from configobj import ConfigObj
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from tests import DBTestCaseMixin, config_path

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