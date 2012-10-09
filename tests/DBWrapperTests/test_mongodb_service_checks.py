from copy import deepcopy
from datetime import datetime
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBServiceChecks(DBTestCase):
    def test_get_all_service_checks(self):
        wrapper_result = self.db_wrapper.get_all_service_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'service']
        for item in expected_result:
            del item['type']
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_get_specific_service_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'service'][0]
        result_id = expected_result['id']
        del expected_result['type'], expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_service_check(result_id)[0]
        assert wrapper_result == expected_result

    def test_get_specific_service_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_service_check('NonexistantServiceUp')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_service_check(self):
        self.db_wrapper.create_service_check('NginxUp', 'Checks if nginx is up', 'MongoDB', 'SampleServiceCheck')
        wrapper_result = list(self.db.active_checks.find({'id': 'NginxUp', 'type': 'service'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = [{
            "description": 'Checks if nginx is up',
            "machine": 'MongoDB',
            "class_name": 'SampleServiceCheck'
        }]
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_create_service_check_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_service_check('MongoDBUp', 'Checks whether MongoDB is up.', 'MongoDB', 'SampleServiceCheck')

    def test_modify_service_check(self):
        self.db_wrapper.modify_service_check('EmailUp', description='Checks if the email server is up', machine='Redis')
        wrapper_result = list(self.db.active_checks.find({'id': 'EmailUp', 'type': 'service'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = [{
            "description": 'Checks if the email server is up',
            "machine": 'Redis',
            "class_name": 'SampleServiceCheck'
        }]
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_modify_service_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_service_check('NonexistantServiceUp', description='Check whether a nonexistant service is up.', machine='MongoDB', class_name='SampleServiceCheck')

    def test_complete_service_check(self):
        time = self.floor_time_to_milliseconds(datetime.now())
        self.db_wrapper.complete_service_check('MongoDBUp', '1', time, 0)
        wrapper_result = list(self.db.completed_checks.find({'id': 'MongoDBUp', 'type': 'service', 'team_id': '1', 'timestamp': time}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0, 'timestamp': 0}))[0]
        expected_result = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'service' and obj['id'] == 'MongoDBUp'][0]
        del expected_result['id'], expected_result['type'], expected_result['machine'], expected_result['class_name']
        expected_result['score'] = 0
        show_difference_between_dicts(wrapper_result, expected_result)
        assert wrapper_result == expected_result

    def test_delete_service_check(self):
        self.db_wrapper.delete_service_check('DeadThingUp')
        wrapper_result = list(self.db.active_checks.find({'id': 'DeadThingUp', 'type': 'service'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_service_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_service_check('NonexistantServiceCheck')