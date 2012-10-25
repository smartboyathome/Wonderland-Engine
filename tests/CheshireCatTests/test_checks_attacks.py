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
from tests.CheshireCatTests import FlaskTestCase

class TestRestTeamsInterface(FlaskTestCase):
    def test_get_all_attack_checks_for_specific_team(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/attacks/teams/1')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '1']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['team_id'], i['type']
            convert_all_datetime_to_timestamp(i, ['timestamp', 'time_to_check'])
        assert json_result == expected_result

    def test_get_all_attack_checks_for_specific_team_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/attacks/teams/1', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_attack_check_for_specific_team(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/checks/attacks/MySecurityHole/teams/1')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '1' and obj['id'] == 'MySecurityHole']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in expected_result:
            del i['team_id'], i['type'], i['id']
            convert_all_datetime_to_timestamp(i, ['timestamp', 'time_to_check'])
        assert json_result == expected_result

    def test_get_specific_attack_check_for_specific_team_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/checks/attacks/MySecurityHole/teams/1', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_attack_check_for_team(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "AnotherSecurityHole",
            "description": "Just another security hole",
            "machine": "Apache",
            "class_name": "SampleAttackerCheck"
        }
        result_data = [{
            "description": "Just another security hole",
            "machine": "Apache",
            "class_name": "SampleAttackerCheck"
        }]
        post = self.app.post('/checks/attacks/teams/6', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/checks/attacks/AnotherSecurityHole/teams/6'
        result = self.app.get('/checks/attacks/AnotherSecurityHole/teams/6')
        print result.status_code, result.data
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_attack_check_for_team_exists(self):
        self.login_user('admin', 'admin')
        query_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '1'][0]
        del query_data['team_id'], query_data['type']
        result_data = {
            "type": "Exists",
            "reason": "An attacker check with the id 'MySecurityHole' for team '1' already exists"
        }
        post = self.app.post('/checks/attacks/teams/1', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_attack_check_for_team_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "AnotherSecurityHole",
            "description": "Just another security hole",
            "machine": "Apache",
            "class_name": "SampleAttackerCheck",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/checks/attacks/teams/6', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/attacks/AnotherSecurityHole/teams/6')
        print result.status_code, result.data
        assert result.status_code == 404

    def test_create_attack_check_for_team_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "description": "Just another security hole",
            "machine": "Apache",
            "class_name": "SampleAttackerCheck"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        expected_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '6']
        for i in expected_data:
            del i['team_id'], i['type']
        post = self.app.post('/checks/attacks/teams/6', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/checks/attacks/teams/6')
        assert result.status_code == 200
        result_data = json.loads(result.data)
        print result_data, expected_data
        assert len(result_data) == len(expected_data)
        assert result_data == expected_data

    def test_create_attack_check_for_team_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/checks/attacks/teams/6', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_attack_check_for_team(self):
        self.login_user('admin', 'admin')
        query_data = {
            'description': 'Checks whether my security hole is still there.',
            'machine': 'Apache',
            'class_name': 'SampleAttackerCheck'
        }
        result_data = [{
            'description': 'Checks whether my security hole is still there.',
            'machine': 'Apache',
            'class_name': 'SampleAttackerCheck'
        }]
        patch = self.app.patch('/checks/attacks/MySecurityHole/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/attacks/MySecurityHole/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_attack_check_for_team_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            'id': 'MySecurityHole',
            'description': 'Checks whether my security hole is still there.',
            'machine': 'Apache',
            'class_name': 'SampleAttackerCheck'
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '2' and obj['id'] == 'MySecurityHole']
        for i in result_data:
            del i['team_id'], i['type'], i['id']
        patch = self.app.patch('/checks/attacks/MySecurityHole/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/checks/attacks/MySecurityHole/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_attack_check_for_team_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['active_checks'] if obj['type'] == 'attacker' and obj['team_id'] == '2' and obj['id'] == 'MySecurityHole']
        for i in result_data:
            del i['team_id'], i['type'], i['id']
        patch = self.app.patch('/checks/attacks/MySecurityHole/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/checks/attacks/MySecurityHole/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_attack_check_for_team_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/checks/attacks/MySecurityHole/teams/2')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_team_data(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/checks/attacks/MongoDBExploit/teams/6')
        assert before_result.status_code == 200
        delete = self.app.delete('/checks/attacks/MongoDBExploit/teams/6')
        assert delete.status_code == 204
        after_result = self.app.get('/checks/attacks/MongoDBExploit/teams/6')
        assert after_result.status_code == 404

    def test_delete_team_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/checks/attacks/MongoDBExploit/teams/6', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data
        before_result = self.app.get('/checks/attacks/MongoDBExploit/teams/6')
        assert before_result.status_code == 200