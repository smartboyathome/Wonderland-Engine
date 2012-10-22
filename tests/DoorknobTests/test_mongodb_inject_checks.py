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
from datetime import timedelta, datetime
from Doorknob.Exceptions import Exists, DoesNotExist
from tests.DoorknobTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBInjectChecks(DBTestCase):
    def test_get_all_inject_checks(self):
        wrapper_result = self.db_wrapper.get_all_inject_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject']
        for item in expected_result:
            del item['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
        assert wrapper_result == expected_result

    def test_get_specific_inject_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject'][0]
        result_id = expected_result['id']
        del expected_result['type'], expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_inject_check(result_id)[0]
        self.correct_imprecise_time(wrapper_result, expected_result, 'time_to_check')
        assert wrapper_result == expected_result

    def test_get_specific_inject_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_inject_check('NonexistantInject')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_inject_check(self):
        time_to_check = datetime.now() + timedelta(seconds=15)
        self.db_wrapper.create_inject_check('CompletedVirusScan', 'Check if teams completed a virus scan', 'Redis', 'SampleInjectCheck', 4993, time_to_check)
        wrapper_result = list(self.db.active_checks.find({'id': 'CompletedVirusScan', 'type': 'inject'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = [{
            "description": 'Check if teams completed a virus scan',
            "machine": 'Redis',
            "class_name": 'SampleInjectCheck',
            'inject_number': 4993,
            'time_to_check': time_to_check
        }]
        assert len(wrapper_result) == len(expected_result)
        self.correct_imprecise_time(wrapper_result[0], expected_result[0], 'time_to_check')
        assert wrapper_result == expected_result

    def test_create_inject_check_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_inject_check('RemovedFiles', 'Checks whether plans were ruined.', 'MongoDB', 'SampleInjectCheck', 4993, datetime.now())

    def test_modify_inject_check(self):
        time_to_check = datetime.now() + timedelta(seconds=15)
        self.db_wrapper.modify_inject_check('AdjustedSpamFilter', description='Checks if the spam was caught', machine='Redis', time_to_check=time_to_check)
        wrapper_result = list(self.db.active_checks.find({'id': 'AdjustedSpamFilter', 'type': 'inject'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = [{
            "description": 'Checks if the spam was caught',
            "machine": 'Redis',
            "class_name": 'SampleInjectCheck',
            "inject_number": '14',
            "time_to_check": time_to_check
        }]
        assert len(wrapper_result) == len(expected_result)
        self.correct_imprecise_time(wrapper_result[0], expected_result[0], 'time_to_check')
        assert wrapper_result == expected_result

    def test_modify_inject_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_inject_check('NonexistantInject', description='Check whether a nonexistant inject was done.', machine='Redis', class_name='SampleInjectCheck')

    def test_complete_inject_check(self):
        time = self.floor_time_to_milliseconds(datetime.now())
        self.db_wrapper.complete_inject_check('RemovedFiles', '2', time, 0)
        wrapper_result = list(self.db.completed_checks.find({'id': 'RemovedFiles', 'type': 'inject', 'team_id': '2', 'timestamp': time}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0, 'timestamp': 0}))[0]
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles'][0]
        del expected_result['id'], expected_result['type'], expected_result['machine'], expected_result['class_name']
        expected_result['score'] = 0
        self.correct_imprecise_time(wrapper_result, expected_result, 'time_to_check')
        assert wrapper_result == expected_result

    def test_delete_inject_check(self):
        self.db_wrapper.delete_inject_check('UnspecifiedInject')
        wrapper_result = list(self.db.active_checks.find({'id': 'UnspecifiedInject', 'type': 'inject'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_inject_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_inject_check('NonexistantInject')