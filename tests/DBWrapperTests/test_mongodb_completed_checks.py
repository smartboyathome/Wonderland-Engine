from copy import deepcopy
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBCompletedChecks(DBTestCase):
    def test_get_all_completed_checks(self):
        wrapper_result = self.db_wrapper.get_all_completed_checks()
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_service_checks(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'service']
        for result in expected_result:
            del result['type']
        wrapper_result = self.db_wrapper.get_all_completed_service_checks()
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_inject_checks(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'inject']
        for result in expected_result:
            del result['type']
        wrapper_result = self.db_wrapper.get_all_completed_inject_checks()
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_attacker_checks(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'attacker']
        for result in expected_result:
            del result['type']
        wrapper_result = self.db_wrapper.get_all_completed_attacker_checks()
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_manual_checks(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'manual']
        for result in expected_result:
            del result['type']
        wrapper_result = self.db_wrapper.get_all_completed_manual_checks()
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_checks_for_team(self):
        wrapper_result = self.db_wrapper.get_all_completed_checks_for_team('1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['team_id'] == '1']
        for result in expected_result:
            del result['team_id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_service_checks_for_team(self):
        wrapper_result = self.db_wrapper.get_all_completed_service_checks_for_team('1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'service']
        for result in expected_result:
            del result['team_id'], result['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_inject_checks_for_team(self):
        wrapper_result = self.db_wrapper.get_all_completed_inject_checks_for_team('1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'inject']
        for result in expected_result:
            del result['team_id'], result['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_attacker_checks_for_team(self):
        wrapper_result = self.db_wrapper.get_all_completed_attacker_checks_for_team('1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'attacker']
        for result in expected_result:
            del result['team_id'], result['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_all_completed_manual_checks_for_team(self):
        wrapper_result = self.db_wrapper.get_all_completed_manual_checks_for_team('1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'manual']
        for result in expected_result:
            del result['team_id'], result['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_completed_service_check_for_team(self):
        wrapper_result = self.db_wrapper.get_specific_completed_service_check_for_team('MongoDBUp', '1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'service' and obj['id'] == 'MongoDBUp']
        for result in expected_result:
            del result['team_id'], result['type'], result['id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_completed_inject_check_for_team(self):
        wrapper_result = self.db_wrapper.get_specific_completed_inject_check_for_team('RemovedFiles', '1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'inject' and obj['id'] == 'RemovedFiles']
        for result in expected_result:
            del result['team_id'], result['type'], result['id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_completed_attacker_check_for_team(self):
        wrapper_result = self.db_wrapper.get_specific_completed_attacker_check_for_team('MySecurityHole', '1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'attacker' and obj['id'] == 'MySecurityHole']
        for result in expected_result:
            del result['team_id'], result['type'], result['id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_completed_manual_check_for_team(self):
        wrapper_result = self.db_wrapper.get_specific_completed_manual_check_for_team('BoardPresentation', '1')
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'manual' and obj['id'] == 'BoardPresentation']
        for result in expected_result:
            del result['team_id'], result['type'], result['id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
            if 'timestamp' in wrapper_result[i] and 'timestamp' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_completed_service_check_for_team_at_time(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'service' and obj['id'] == 'MongoDBUp'][0]
        expected_result['timestamp'] = self.floor_time_to_milliseconds(expected_result['timestamp'])
        wrapper_result = self.db_wrapper.get_specific_completed_service_check_for_team_at_time(expected_result['id'],
            expected_result['team_id'], expected_result['timestamp'])[0]
        del expected_result['team_id'], expected_result['type'], expected_result['id'], expected_result['timestamp']
        assert wrapper_result == expected_result

    def test_get_specific_completed_attacker_check_for_team_at_time(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks']
                           if obj['team_id'] == '1' and obj['type'] == 'attacker' and obj['id'] == 'MySecurityHole'][0]
        expected_result['timestamp'] = self.floor_time_to_milliseconds(expected_result['timestamp'])
        wrapper_result = self.db_wrapper.get_specific_completed_attacker_check_for_team_at_time(expected_result['id'],
            expected_result['team_id'], expected_result['timestamp'])[0]
        del expected_result['team_id'], expected_result['type'], expected_result['id'], expected_result['timestamp']
        assert wrapper_result == expected_result