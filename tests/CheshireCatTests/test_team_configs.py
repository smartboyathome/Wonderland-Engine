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
import json
from tests import show_difference_between_dicts
from tests.CheshireCatTests import FlaskTestCase

class TestRestTeamConfigsInterface(FlaskTestCase):
    def test_get_specific_teams_configs(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/teams/1/configs')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1']
        for result in expected_result:
            del result['team_id']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        assert json_result == expected_result

    def test_get_specific_team_configs_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/1/configs', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_team_config_for_machine(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/teams/1/configs/MongoDB')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'MongoDB'][0]
        del expected_result['team_id'], expected_result['machine_id']
        assert json.loads(rest_result.data) == expected_result

    def test_get_specific_team_config_for_machine_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/1/configs/MongoDB', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_team_config_for_machine(self):
        self.login_user('admin', 'admin')
        query_data = {
            "machine_id": "MongoDB",
            "username": "team6",
            "password": "team6mongo",
            "port": "27017"
        }
        result_data = {
            "username": "team6",
            "password": "team6mongo",
            "port": "27017"
        }
        post = self.app.post('/teams/6/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/teams/6/configs/MongoDB'
        result = self.app.get('/teams/6/configs/MongoDB')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_team_config_for_machine_exists(self):
        self.login_user('admin', 'admin')
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
        post = self.app.post('/teams/1/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_team_config_for_machine_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "team_id": "6",
            "machine_id": "Redis",
            "username": "team6",
            "password": "team6mongo",
            "port": "27017"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'team_id' is not valid for this interface."
        }
        post = self.app.post('/teams/6/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/teams/6/configs/Redis')
        assert result.status_code == 404

    def test_create_team_config_for_machine_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "username": "team6",
            "password": "team6mongo",
            "port": "27017"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'machine_id' is not specified."
        }
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '6']
        for result in expected_result:
            del result['team_id']
        post = self.app.post('/teams/6/configs', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/teams/6/configs')
        assert result.status_code == 200
        assert json.loads(result.data) == expected_result

    def test_create_team_config_for_machine_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/teams/6/configs', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_team_config_for_machine(self):
        self.login_user('admin', 'admin')
        query_data = {
            "username": "newteam1",
            "password": "newteam1apache"
        }
        expected_result = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'Apache'][0]
        expected_result['username'] = 'newteam1'
        expected_result['password'] = 'newteam1apache'
        del expected_result['team_id'], expected_result['machine_id']
        patch = self.app.patch('/teams/1/configs/Apache', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/teams/1/configs/Apache')
        assert result.status_code == 200
        assert json.loads(result.data) == expected_result

    def test_modify_team_config_for_machine_invalid_param(self):
        self.login_user('admin', 'admin')
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
        patch = self.app.patch('/teams/1/configs/Redis', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/teams/1/configs/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_config_for_machine_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = [obj for obj in self.data['team_configs'] if obj['team_id'] == '1' and obj['machine_id'] == 'Redis'][0]
        del result_data['team_id'], result_data['machine_id']
        patch = self.app.patch('/teams/1/configs/Redis', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/teams/1/configs/Redis')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_config_for_machine_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/teams/1/configs/Redis')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_team_config_for_machine(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/teams/2/configs/Redis')
        assert before_result.status_code == 200
        delete = self.app.delete('/teams/2/configs/Redis')
        assert delete.status_code == 204
        after_result = self.app.get('/teams/2/configs/Redis')
        assert after_result.status_code == 404

    def test_delete_team_config_for_machine_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/teams/2/configs/MongoDB', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data
        before_result = self.app.get('/teams/2/configs/MongoDB')
        assert before_result.status_code == 200