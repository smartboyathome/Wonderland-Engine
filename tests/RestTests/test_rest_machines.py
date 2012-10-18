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

import json
from tests.RestTests import FlaskTestCase

class TestRestMachinesInterface(FlaskTestCase):
    def test_get_all_machines_data(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/machines/')
        assert result.status_code == 200
        assert json.loads(result.data) == self.data['machines']

    def test_get_all_machines_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/machines/', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_machine_data(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/machines/MongoDB')
        result_data = [obj for obj in self.data['machines'] if obj['id'] == 'MongoDB'][0]
        del result_data['id']
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_get_specific_machine_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/machines/MongoDB', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_machine_data(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "Dovecot",
            "general_ip": "127.0.0.4"
        }
        result_data = {
            "general_ip": "127.0.0.4"
        }
        post = self.app.post('/machines/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/machines/Dovecot'
        result = self.app.get('/machines/Dovecot')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_machine_data_exists(self):
        self.login_user('admin', 'admin')
        query_data = {
            'id': 'MongoDB',
            'general_ip': '127.0.0.1'
        }
        result_data = {
            "type": "Exists",
            "reason": "A machine with the id 'MongoDB' already exists"
        }
        post = self.app.post('/machines/', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_machine_data_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "Dovecot",
            "general_ip": "127.0.0.4",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/machines/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/machines/Dovecot')
        assert result.status_code == 404

    def test_create_machine_data_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "general_ip": "127.0.0.4"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        result_data = self.data['machines']
        post = self.app.post('/machines/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/machines/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_machine_data_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/machines/', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_machine_data(self):
        self.login_user('admin', 'admin')
        query_data = {
            "general_ip": "127.0.0.254"
        }
        result_data = {
            "general_ip": "127.0.0.254"
        }
        patch = self.app.patch('/machines/Redis', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/machines/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_machine_data_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "Redis",
            "general_ip": "127.0.0.254"
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = [obj for obj in self.data['machines'] if obj['id'] == 'Redis'][0]
        del result_data['id']
        patch = self.app.patch('/machines/Redis', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/machines/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_machine_data_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['machines'] if obj['id'] == 'Redis'][0]
        del result_data['id']
        patch = self.app.patch('/machines/Redis', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/machines/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_machine_data_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/machines/Redis')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_machine_data(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/machines/Apache')
        assert before_result.status_code == 200
        delete = self.app.delete('/machines/Apache')
        assert delete.status_code == 204
        after_result = self.app.get('/machines/Apache')
        assert after_result.status_code == 404

    def test_delete_machine_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/machines/Apache', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data