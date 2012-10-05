from copy import deepcopy
from datetime import timedelta, datetime
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBInjectChecks(DBTestCase):
    def correct_imprecise_time(self, wrapper_result, expected_result):
        # MongoDB stores time less precisely than Python, so the following function is needed.
        assert expected_result['time_to_check'] - wrapper_result['time_to_check'] < timedelta(seconds=0.001)
        expected_result['time_to_check'] = wrapper_result['time_to_check']

    def test_get_all_inject_checks(self):
        wrapper_result = self.db_wrapper.get_all_inject_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject']
        for item in expected_result:
            del item['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i])
        assert wrapper_result == expected_result

    def test_get_specific_inject_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject'][0]
        result_id = expected_result['id']
        del expected_result['type'], expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_inject_check(result_id)[0]
        self.correct_imprecise_time(wrapper_result, expected_result)
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
        self.correct_imprecise_time(wrapper_result[0], expected_result[0])
        assert wrapper_result == expected_result

    def test_create_inject_check_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_inject_check('RemovedFiles', 'Checks whether plans were ruined.', 'MongoDB', 'SampleInjectCheck', 4993, datetime.now())

    '''def test_modify_service_check(self):
        self.db_wrapper.modify_service_check('EmailUp', description='Checks if the email server is up', machine='Redis')
        wrapper_result = list(self.db.active_checks.find({'id': 'EmailUp', 'type': 'service'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = [{
            "description": 'Checks if the email server is up',
            "machine": 'Redis',
            "class_name": 'SampleServiceCheck'
        }]
        assert len(wrapper_result) != 0
        assert wrapper_result == expected_result

    def test_modify_service_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_service_check('NonexistantServiceUp', description='Check whether a nonexistant service is up.', machine='MongoDB', class_name='SampleServiceCheck')

    def test_delete_service_check(self):
        self.db_wrapper.delete_service_check('DeadThingUp')
        wrapper_result = list(self.db.users.find({'id': 'DeadThingUp', 'type': 'service'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_service_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_service_check('NonexistantServiceCheck')'''