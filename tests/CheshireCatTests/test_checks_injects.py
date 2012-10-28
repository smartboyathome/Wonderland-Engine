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
from copy import deepcopy
from datetime import datetime

import json
from CheshireCat.utils import convert_all_datetime_to_timestamp, convert_all_timestamp_to_datetime, convert_datetime_to_timestamp
from tests import show_difference_between_dicts
from tests.CheshireCatTests import FlaskTestCase

class TestRestChecksInjectsInterface(FlaskTestCase):
    def test_get_all_inject_checks(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/injects')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject']
        convert_all_datetime_to_timestamp(expected_result, ['time_to_check'])
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['type']
        assert json_result == expected_result

    def test_get_all_inject_checks_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/injects', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_inject_checks(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/injects/RemovedFiles')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles']
        convert_all_datetime_to_timestamp(expected_result, ['time_to_check'])
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['id'], i['type']
        assert json_result == expected_result

    def test_get_specific_inject_check_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/injects/RemovedFiles', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_inject_check(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "FileSystemSetUp",
            "description": "Checking if the filesystem was set up on time.",
            "machine": "Apache",
            "class_name": "SampleInjectCheck",
            "inject_number": "66",
            "time_to_check": convert_datetime_to_timestamp(datetime.now())
        }
        expected_result = [{
            "description": "Checking if the filesystem was set up on time.",
            "machine": "Apache",
            "class_name": "SampleInjectCheck",
            "inject_number": "66",
            "time_to_check": query_data['time_to_check']
        }]
        post = self.app.post('/checks/injects', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/checks/injects/FileSystemSetUp'
        result = self.app.get('/checks/injects/FileSystemSetUp')
        rest_result = json.loads(result.data)
        show_difference_between_dicts(rest_result[0], expected_result[0])
        assert result.status_code == 200
        assert rest_result == expected_result

    def test_create_inject_check_exists(self):
        self.login_user('admin', 'admin')
        query_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject'][0]
        del query_data['type']
        query_data['time_to_check'] = convert_datetime_to_timestamp(query_data['time_to_check'])
        result_data = {
            "type": "Exists",
            "reason": "A inject check with the id '{}' already exists".format(query_data['id'])
        }
        post = self.app.post('/checks/injects', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_inject_check_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "FileSystemSetUp",
            "description": "Checking if the filesystem was set up on time.",
            "machine": "Apache",
            "class_name": "SampleInjectCheck",
            "inject_number": "66",
            "time_to_check": convert_datetime_to_timestamp(datetime.now()),
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/checks/injects', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/injects/FileSystemSetUp')
        print result.status_code, result.data
        assert result.status_code == 404

    def test_create_inject_check_for_team_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "description": "Checking if the filesystem was set up on time.",
            "machine": "Apache",
            "class_name": "SampleInjectCheck",
            "inject_number": "66",
            "time_to_check": convert_datetime_to_timestamp(datetime.now())
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        expected_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject']
        for i in expected_data:
            del i['type']
            i['time_to_check'] = convert_datetime_to_timestamp(i['time_to_check'])
        post = self.app.post('/checks/injects', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/injects')
        assert result.status_code == 200
        result_data = json.loads(result.data)
        assert len(result_data) == len(expected_data)
        assert result_data == expected_data

    def test_create_inject_check_for_team_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/checks/injects', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_inject_check(self):
        self.login_user('admin', 'admin')
        query_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles'][0]
        del query_data['type'], query_data['id']
        query_data['time_to_check'] = convert_datetime_to_timestamp(query_data['time_to_check'])
        query_data['machine'] = 'Redis'
        query_data['inject_number'] = '57'
        result_data = [query_data]
        patch = self.app.patch('/checks/injects/RemovedFiles', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/injects/RemovedFiles')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_inject_check_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = [deepcopy(obj) for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles'][0]
        del query_data['type']
        query_data['time_to_check'] = convert_datetime_to_timestamp(query_data['time_to_check'])
        query_data['machine'] = 'Redis'
        query_data['inject_number'] = '57'
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles']
        for i in result_data:
            del i['type'], i['id']
            i['time_to_check'] = convert_datetime_to_timestamp(i['time_to_check'])
        patch = self.app.patch('/checks/injects/RemovedFiles', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/checks/injects/RemovedFiles')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_inject_check_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'inject' and obj['id'] == 'RemovedFiles']
        for i in result_data:
            del i['type'], i['id']
            i['time_to_check'] = convert_datetime_to_timestamp(i['time_to_check'])
        patch = self.app.patch('/checks/injects/RemovedFiles', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/injects/RemovedFiles')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_inject_check_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/checks/injects/RemovedFiles')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_inject_check(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/checks/injects/AdjustedSpamFilter')
        assert before_result.status_code == 200
        delete = self.app.delete('/checks/injects/AdjustedSpamFilter')
        assert delete.status_code == 204
        after_result = self.app.get('/checks/injects/AdjustedSpamFilter')
        assert after_result.status_code == 404

    def test_delete_inject_check_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/checks/injects/AdjustedSpamFilter', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data
        before_result = self.app.get('/checks/injects/AdjustedSpamFilter')
        assert before_result.status_code == 200