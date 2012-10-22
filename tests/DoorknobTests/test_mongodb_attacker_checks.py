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
from Doorknob.Exceptions import Exists, DoesNotExist, TeamDoesNotExist
from tests.DoorknobTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBAttackerChecks(DBTestCase):
    def test_get_all_attacker_checks(self):
        wrapper_result = self.db_wrapper.get_all_attacker_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'attacker']
        for item in expected_result:
            del item['type']
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_get_specific_attacker_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'attacker'][0]
        result_id = expected_result['id']
        team_id = expected_result['team_id']
        del expected_result['type'], expected_result['id'], expected_result['team_id']
        wrapper_result = self.db_wrapper.get_specific_attacker_check(result_id, team_id)[0]
        assert wrapper_result == expected_result

    def test_get_specific_attacker_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_attacker_check('NonexistantExploit', '6')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_attacker_check(self):
        self.db_wrapper.create_attacker_check('SSHExploit', 'Checks if the ssh exploit still exists', 'Apache', '2', 'SampleAttackerCheck')
        wrapper_result = list(self.db.active_checks.find({'id': 'SSHExploit', 'type': 'attacker', 'team_id': '2'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = [{
            "description": 'Checks if the ssh exploit still exists',
            "machine": 'Apache',
            "class_name": 'SampleAttackerCheck'
        }]
        assert len(wrapper_result) == len(expected_result)
        show_difference_between_dicts(wrapper_result[0], expected_result[0])
        assert wrapper_result == expected_result

    def test_create_attacker_check_exists(self):
        with self.assertRaises(Exists):
            result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'attacker'][0]
            self.db_wrapper.create_attacker_check(result['id'], result['description'], result['machine'], result['team_id'], result['class_name'])

    def test_create_attacker_check_team_nonexistant(self):
        with self.assertRaises(TeamDoesNotExist):
            self.db_wrapper.create_attacker_check('SomeExploit', 'Checks for some exploit', 'Apache', '999', 'SampleAttackerCheck')

    def test_modify_attacker_check(self):
        self.db_wrapper.modify_attacker_check('MongoDBExploit', '6', description='Checks if the bad exploit for MongoDB was patched')
        wrapper_result = list(self.db.active_checks.find({'id': 'MongoDBExploit', 'type': 'attacker', 'team_id': '6'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = [{
            "description": 'Checks if the bad exploit for MongoDB was patched',
            "machine": 'MongoDB',
            "class_name": 'SampleAttackerCheck'
        }]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_modify_attacker_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_attacker_check('NonexistantExploit', '2', description='Check whether a nonexistant exploit still exists.', machine='Redis', class_name='SampleAttackerCheck')

    def test_complete_attacker_check(self):
        time = self.floor_time_to_milliseconds(datetime.now())
        self.db_wrapper.complete_attacker_check('MySecurityHole', '2', time, 0)
        wrapper_result = list(self.db.completed_checks.find({'id': 'MySecurityHole', 'type': 'attacker', 'team_id': '2', 'timestamp': time}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0, 'timestamp': 0}))[0]
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['id'] == 'MySecurityHole'][0]
        del expected_result['id'], expected_result['type'], expected_result['machine'], expected_result['class_name'], expected_result['team_id']
        expected_result['score'] = 0
        show_difference_between_dicts(wrapper_result, expected_result)
        assert wrapper_result == expected_result

    def test_delete_attacker_check(self):
        self.db_wrapper.delete_attacker_check('BrokenExploit', '2')
        wrapper_result = list(self.db.active_checks.find({'id': 'BrokenExploit', 'type': 'attacker', 'team_id': '2'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_attacker_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_attacker_check('NonexistantExploit', '6')