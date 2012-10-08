from copy import deepcopy
from DBWrappers.Exceptions import Exists, DoesNotExist, TeamDoesNotExist
from tests.DBWrapperTests import DBTestCase
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

    def test_delete_attacker_check(self):
        self.db_wrapper.delete_attacker_check('BrokenExploit', '2')
        wrapper_result = list(self.db.active_checks.find({'id': 'BrokenExploit', 'type': 'attacker', 'team_id': '2'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_attacker_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_attacker_check('NonexistantExploit', '6')