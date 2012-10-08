from copy import deepcopy
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBGeneralChecks(DBTestCase):
    def test_get_all_checks(self):
        wrapper_result = self.db_wrapper.get_all_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks']]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            #show_difference_between_dicts(wrapper_result[i], expected_result[i])
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
        assert wrapper_result == expected_result

    def test_get_specific_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks']][0]
        result_id = expected_result['id']
        result_type = expected_result['type']
        del expected_result['type'], expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_check(result_id, result_type)[0]
        assert wrapper_result == expected_result

    def test_get_specific_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_check('NonexistantCheck', 'any')
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_check(self):
        self.db_wrapper.delete_specific_check('BrokenExploit', 'attacker')
        wrapper_result = list(self.db.active_checks.find({'id': 'BrokenExploit', 'type': 'attacker'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_specific_check('NonexistantServiceCheck', 'service')