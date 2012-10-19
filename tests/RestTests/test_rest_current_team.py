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
from ScoringServer.utils import convert_datetime_to_timestamp
from tests import show_difference_between_dicts
from tests.RestTests import FlaskTestCase

class TestRestCurrentTeamInterface(FlaskTestCase):
    def test_get_current_team_data(self):
        self.login_user('team1', 'uw seattle')
        rest_result = self.app.get('/current_team/')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['teams'] if obj['id'] == '1'][0]
        del expected_result['id']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        assert json_result == expected_result

    def test_get_current_team_data_with_params(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/current_team/', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_current_teams_configs(self):
        self.login_user('team1', 'uw seattle')
        rest_result = self.app.get('/current_team/configs')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1']
        for result in expected_result:
            del result['team_id']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        assert json_result == expected_result

    def test_get_current_team_configs_with_params(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/current_team/configs', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_current_team_config_for_machine(self):
        self.login_user('team1', 'uw seattle')
        rest_result = self.app.get('/current_team/configs/MongoDB')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'MongoDB'][0]
        del expected_result['team_id'], expected_result['machine_id']
        assert json.loads(rest_result.data) == expected_result

    def test_get_current_team_config_for_machine_with_params(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/current_team/configs/MongoDB', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_current_team_config_for_machine(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "machine_id": "DomainController",
            "username": "team1",
            "password": "team1ldap",
            "port": "389"
        }
        result_data = {
            "username": "team1",
            "password": "team1ldap",
            "port": "389"
        }
        post = self.app.post('/current_team/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/current_team/configs/DomainController'
        result = self.app.get('/current_team/configs/DomainController')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_current_team_config_for_machine_exists(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "machine_id": "MongoDB",
            "username": "team1",
            "password": "team1mongo",
            "port": "27017"
        }
        result_data = {
            "type": "Exists",
            "reason": "A config for team '1' machine 'MongoDB' already exists"
        }
        post = self.app.post('/current_team/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_current_team_config_for_machine_invalid_param(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "team_id": "1",
            "machine_id": "DomainController",
            "username": "team1",
            "password": "team1ldap",
            "port": "389"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'team_id' is not valid for this interface."
        }
        post = self.app.post('/current_team/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/current_team/configs/DomainController')
        assert result.status_code == 404

    def test_create_current_team_config_for_machine_missing_param(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "username": "team1",
            "password": "team1ldap",
            "port": "389"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'machine_id' is not specified."
        }
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1']
        for result in expected_result:
            del result['team_id']
        post = self.app.post('/current_team/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/current_team/configs')
        assert result.status_code == 200
        assert json.loads(result.data) == expected_result

    def test_create_current_team_config_for_machine_no_data(self):
        self.login_user('team1', 'uw seattle')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/current_team/configs', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_team_config_for_machine(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "username": "newteam1",
            "password": "newteam1apache"
        }
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'Apache'][0]
        expected_result['username'] = 'newteam1'
        expected_result['password'] = 'newteam1apache'
        del expected_result['team_id'], expected_result['machine_id']
        patch = self.app.patch('/current_team/configs/Apache', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/current_team/configs/Apache')
        assert result.status_code == 200
        assert json.loads(result.data) == expected_result

    def test_modify_current_team_config_for_machine_invalid_param(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "team_id": "1",
            "machine_id": "Redis",
            "username": "newteam1",
            "password": "newteam1redis"
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameters 'team_id', 'machine_id' are not valid for this interface."
        }
        result_data = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'Redis'][0]
        del result_data['team_id'], result_data['machine_id']
        patch = self.app.patch('/current_team/configs/Redis', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/current_team/configs/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_current_team_config_for_machine_no_param(self):
        self.login_user('team1', 'uw seattle')
        query_data = {}
        result_data = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'Redis'][0]
        del result_data['team_id'], result_data['machine_id']
        patch = self.app.patch('/current_team/configs/Redis', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/current_team/configs/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_config_for_machine_no_data(self):
        self.login_user('team1', 'uw seattle')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/current_team/configs/Redis')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_current_team_config_for_machine(self):
        self.login_user('team1', 'uw seattle')
        before_result = self.app.get('/current_team/configs/Apache')
        assert before_result.status_code == 200
        delete = self.app.delete('/current_team/configs/Apache')
        assert delete.status_code == 204
        after_result = self.app.get('/current_team/configs/Apache')
        assert after_result.status_code == 404

    def test_delete_current_team_config_for_machine_with_params(self):
        self.login_user('team1', 'uw seattle')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/current_team/configs/MongoDB', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data
        before_result = self.app.get('/current_team/configs/MongoDB')
        assert before_result.status_code == 200