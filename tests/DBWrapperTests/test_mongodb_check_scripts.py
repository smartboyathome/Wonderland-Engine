from copy import deepcopy
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBCheckScripts(DBTestCase):
    def test_get_all_check_scripts(self):
        wrapper_result = self.db_wrapper.get_all_check_scripts()
        expected_result = [deepcopy(obj) for obj in self.data['check_scripts']]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_get_specific_check_script(self):
        expected_result = [deepcopy(obj) for obj in self.data['check_scripts']][0]
        result_id = expected_result['id']
        del expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_check_script(result_id)[0]
        assert wrapper_result == expected_result

    def test_get_specific_check_script_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_service_check('NonexistantScript')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_check_script(self):
        self.db_wrapper.create_check_script('MoreServiceChecks', '/example/path/MoreServiceChecks.py')
        wrapper_result = list(self.db.check_scripts.find({'id': 'MoreServiceChecks'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'path': '/example/path/MoreServiceChecks.py'
        }]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_create_check_script_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_check_script('InjectChecks', '/example/path/InjectChecks.py')

    def test_modify_check_script(self):
        self.db_wrapper.modify_check_script('InjectChecks', path='/example/path/InjectChecks2.py')
        wrapper_result = list(self.db.check_scripts.find({'id': 'InjectChecks'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'path': '/example/path/InjectChecks2.py'
        }]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_modify_check_script_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_check_script('NonexistantScript', path='/some/malicious/script.py')

    def test_delete_check_script(self):
        self.db_wrapper.delete_check_script('Attacker1Checks')
        wrapper_result = list(self.db.check_scripts.find({'id': 'Attacker1Checks'}, {'_id': 0, 'id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_check_script_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_check_script('NonexistantScript')