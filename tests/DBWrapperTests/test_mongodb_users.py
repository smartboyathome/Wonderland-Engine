from copy import deepcopy
import hashlib
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests import DBTestCase

class TestMongoDBUsers(DBTestCase):
    def test_get_all_users(self):
        wrapper_result = self.db_wrapper.get_all_users()
        expected_result = deepcopy(self.data['users'])
        for user in expected_result:
            del user['password']
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_get_specific_user(self):
        wrapper_result = self.db_wrapper.get_specific_user('team1')
        expected_result = [deepcopy(user) for user in self.data['users'] if user['id'] == 'team1']
        for user in expected_result:
            del user['id'], user['password']
        assert wrapper_result == expected_result

    def test_get_specific_user_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_user('team999')
        expected_result = []
        assert wrapper_result == expected_result

    def test_get_specific_user_right_password(self):
        wrapper_result = self.db_wrapper.get_specific_user('team1', hashlib.md5('uw seattle').hexdigest())
        expected_result = [deepcopy(user) for user in self.data['users'] if user['id'] == 'team1' and user['password'] == hashlib.md5('uw seattle').hexdigest()]
        for user in expected_result:
            del user['id'], user['password']
        assert wrapper_result == expected_result

    def test_get_specific_user_wrong_password(self):
        wrapper_result = self.db_wrapper.get_specific_user('team1', hashlib.md5("h4xx0r3d").hexdigest())
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_user(self):
        self.db_wrapper.create_user('team2', hashlib.md5('western wa').hexdigest(), 'team2@example.com', 'team', team='2')
        wrapper_result = list(self.db.users.find({'id': 'team2'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'password': hashlib.md5('western wa').hexdigest(),
            'email': 'team2@example.com',
            'role': 'team',
            'team': '2'
        }]
        assert wrapper_result == expected_result

    def test_create_user_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_user('team1', hashlib.md5('western wa').hexdigest(), 'team1@example.com', 'team', team='1')

    def test_modify_user(self):
        self.db_wrapper.modify_user('admin', password=hashlib.md5('h4xx0r3d').hexdigest(), email='h4xx0rz@example.com')
        wrapper_result = list(self.db.users.find({'id': 'admin'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'password': hashlib.md5('h4xx0r3d').hexdigest(),
            'email': 'h4xx0rz@example.com',
            'role': 'administrator'
        }]
        assert wrapper_result == expected_result

    def test_modify_user_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_user('FAILURE', password=hashlib.md5('h4xx0r3d').hexdigest(), email='h4xx0rz@example.com')

    def test_delete_user(self):
        self.db_wrapper.delete_user('white_team')
        wrapper_result = list(self.db.users.find({'id': 'white_team'}, {'_id': 0, 'id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_user_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_user('FAILURE')