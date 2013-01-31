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
import pymongo, os

__all__=['config_path', 'DBTestCaseMixin', 'show_difference_between_dicts']

config_path = os.path.join(os.path.dirname(__file__), 'testing.cfg')

from tests.db_data import generate_db_data

class DBTestCaseMixin(object):
    def init_db_data(self, db_host, db_port, db_name):
        self.db = pymongo.Connection(db_host, int(db_port), safe=True)[db_name]
        if db_name in self.db.connection.database_names():
            #teardown wasn't run last time, so lets run it now.
            self.drop_db_data()
        self.data = generate_db_data()
        for key in self.data:
            mongodb_data = deepcopy(self.data[key])
            self.db[key].insert(mongodb_data)

    def drop_db_data(self):
        self.db.connection.drop_database(self.db.name)

def show_difference_between_dicts(first, second):
    different_keys = {}
    different_values = {}
    for key in set(first.keys()+second.keys()):
        if key not in first:
            different_keys[key] = 'first'
        elif key not in second:
            different_keys[key] = 'second'
        elif first[key] != second[key]:
            different_values[key] = (first[key], second[key])
    for key in different_keys:
        print "The key '{}' does not exist in the {} dict".format(key, different_keys[key])
    for key in different_values:
        print "Difference in values for key '{}': '{}' (of type '{}') vs '{}' (of type '{}')".format(key, different_values[key][0], type(different_values[key][0]).__name__, different_values[key][1], type(different_values[key][1]).__name__)