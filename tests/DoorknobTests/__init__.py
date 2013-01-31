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

from datetime import timedelta, datetime
import unittest
from configobj import ConfigObj
from Doorknob.MongoDBWrapper import MongoDBWrapper
from .. import DBTestCaseMixin, config_path

class DBTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        print config_path
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