from datetime import timedelta, datetime
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

    def correct_imprecise_time(self, wrapper_result, expected_result, key):
        # MongoDB stores time less precisely than Python, so the following function is needed.
        assert expected_result[key] - wrapper_result[key] < timedelta(microseconds=1000)
        expected_result[key] = wrapper_result[key]

    def floor_time_to_milliseconds(self, time):
        return datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, (time.microsecond // 1000)*1000)