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
from CheshireCat.utils import convert_all_datetime_to_timestamp
from tests import show_difference_between_dicts
from tests.CheshireCatTests import FlaskTestCase

class TestRestChecksServicesInterface(FlaskTestCase):
    def test_get_all_service_checks(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/services')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'service']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['type']
        assert json_result == expected_result

    def test_get_all_service_checks_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/services', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_service_checks(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/services/MongoDBUp')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'service' and obj['id'] == 'MongoDBUp']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['id'], i['type']
        assert json_result == expected_result

    def test_get_specific_service_check_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/services/MongoDBUp', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_service_check(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "SomeServiceUp",
            "description": "Checking if SomeService is up",
            "machine": "Apache",
            "class_name": "SampleServiceCheck"
        }
        result_data = [{
            "description": "Checking if SomeService is up",
            "machine": "Apache",
            "class_name": "SampleServiceCheck"
        }]
        post = self.app.post('/checks/services', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/checks/services/SomeServiceUp'
        result = self.app.get('/checks/services/SomeServiceUp')
        print result.status_code, result.data
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_service_check_exists(self):
        self.login_user('admin', 'admin')
        query_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'service'][0]
        del query_data['type']
        result_data = {
            "type": "Exists",
            "reason": "A service check with the id '{}' already exists".format(query_data['id'])
        }
        post = self.app.post('/checks/services', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_service_check_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "SomeServiceUp",
            "description": "Checking if SomeService is up",
            "machine": "Apache",
            "class_name": "SampleServiceCheck",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/checks/services', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/services/SomeServiceUp')
        print result.status_code, result.data
        assert result.status_code == 404

    def test_create_service_check_for_team_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "description": "Checking if SomeService is up",
            "machine": "Apache",
            "class_name": "SampleServiceCheck"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        expected_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'service']
        for i in expected_data:
            del i['type']
        post = self.app.post('/checks/services', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/services')
        assert result.status_code == 200
        result_data = json.loads(result.data)
        print result_data, expected_data
        assert len(result_data) == len(expected_data)
        assert result_data == expected_data

    def test_create_service_check_for_team_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/checks/services', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_service_check(self):
        self.login_user('admin', 'admin')
        query_data = {
            'description': 'Checks whether the MongoDB service is really running.',
            'machine': 'Apache',
            'class_name': 'SampleServiceCheck'
        }
        result_data = [{
            'description': 'Checks whether the MongoDB service is really running.',
            'machine': 'Apache',
            'class_name': 'SampleServiceCheck'
        }]
        patch = self.app.patch('/checks/services/MongoDBUp', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/services/MongoDBUp')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_service_check_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            'id': 'MongoDBUp',
            'description': 'Checks whether the MongoDB service is really running.',
            'machine': 'Apache',
            'class_name': 'SampleServiceCheck'
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'service' and obj['id'] == 'MongoDBUp']
        for i in result_data:
            del i['type'], i['id']
        patch = self.app.patch('/checks/services/MongoDBUp', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/checks/services/MongoDBUp')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_service_check_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'service' and obj['id'] == 'MongoDBUp']
        for i in result_data:
            del i['type'], i['id']
        patch = self.app.patch('/checks/services/MongoDBUp', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/services/MongoDBUp')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_service_check_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/checks/services/MongoDBUp')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_service_check(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/checks/services/EmailUp')
        assert before_result.status_code == 200
        delete = self.app.delete('/checks/services/EmailUp')
        assert delete.status_code == 204
        after_result = self.app.get('/checks/services/EmailUp')
        assert after_result.status_code == 404

    def test_delete_service_check_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/checks/services/EmailUp', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data
        before_result = self.app.get('/checks/services/EmailUp')
        assert before_result.status_code == 200