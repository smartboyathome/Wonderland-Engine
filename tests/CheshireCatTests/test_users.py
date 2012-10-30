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
import hashlib

import json
from tests import show_difference_between_dicts
from tests.CheshireCatTests import FlaskTestCase

class TestRestUsersInterface(FlaskTestCase):
    def test_get_all_users(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/users/')
        assert result.status_code == 200
        json_result = json.loads(result.data)
        expected_result = self.data['users']
        for i in expected_result:
            del i['password']
        assert len(json_result) == len(expected_result)
        assert json_result == self.data['users']

    def test_get_all_users_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/users/', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_all_users_with_role(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/users/roles/administrator')
        result_data = [obj for obj in self.data['users'] if obj['role'] == 'administrator']
        for i in result_data:
            del i['role'], i['password']
        assert result.status_code == 200
        json_result = json.loads(result.data)
        assert len(json_result) == len(result_data)
        for i, j in zip(json_result, result_data):
            show_difference_between_dicts(i, j)
        assert json_result == result_data

    def test_get_specific_users_with_role_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/users/roles/administrator', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_user(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/users/team1')
        result_data = [obj for obj in self.data['users'] if obj['id'] == 'team1'][0]
        del result_data['id'], result_data['password']
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_get_specific_user_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/users/team1', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_team_user(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "team6",
            "password": "uw bothell",
            "email": "team6@example.com",
            "role": "team",
            "team": "6"
        }
        result_data = {
            "email": "team6@example.com",
            "role": "team",
            "team": "6"
        }
        post = self.app.post('/users/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/users/team6'
        result = self.app.get('/users/team6')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_org_user(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "organizers",
            "password": "the_leaders",
            "email": "organizers@example.com",
            "role": "organizer"
        }
        result_data = {
            "email": "organizers@example.com",
            "role": "organizer"
        }
        post = self.app.post('/users/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/users/organizers'
        result = self.app.get('/users/organizers')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_user_exists(self):
        self.login_user('admin', 'admin')
        query_data = {
            'id': 'team1',
            'password': 'uw seattle',
            'email': 'team1@example.com',
            'role': 'team',
            'team': '1'
        }
        result_data = {
            "type": "Exists",
            "reason": "A user with the id 'team1' already exists"
        }
        post = self.app.post('/users/', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_user_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "team6",
            "password": "uw bothell",
            "email": "team6@example.com",
            "role": "team",
            "team": "6",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/users/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/users/Dovecot')
        assert result.status_code == 404

    def test_create_user_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "password": "uw bothell",
            "email": "team6@example.com",
            "role": "team",
            "team": "6"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        result_data = self.data['users']
        for i in result_data:
            del i['password']
        post = self.app.post('/users/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/users/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_user_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/users/', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_user(self):
        self.login_user('admin', 'admin')
        query_data = {
            "email": "organizers@example.com"
        }
        result_data = {
            'email': 'organizers@example.com',
            'role': 'organizer'
        }
        patch = self.app.patch('/users/white_team', data=json.dumps(query_data))
        print patch.status_code, patch.data
        assert patch.status_code == 204
        result = self.app.get('/users/white_team')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_user_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "white_team",
            "email": "organizers@example.com"
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = [obj for obj in self.data['users'] if obj['id'] == 'white_team'][0]
        del result_data['id'], result_data['password']
        patch = self.app.patch('/users/white_team', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/users/white_team')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_user_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['users'] if obj['id'] == 'white_team'][0]
        del result_data['id'], result_data['password']
        patch = self.app.patch('/users/white_team', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/users/white_team')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_user_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/users/white_team')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_user(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/users/evil_red_team')
        assert before_result.status_code == 200
        delete = self.app.delete('/users/evil_red_team')
        assert delete.status_code == 204
        after_result = self.app.get('/users/evil_red_team')
        assert after_result.status_code == 404

    def test_delete_user_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/users/evil_red_team', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data