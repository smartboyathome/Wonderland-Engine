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

from . import FlaskTestCase
import json

class TestRestTeamsInterface(FlaskTestCase):
    def test_get_all_teams_data(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/teams/')
        assert result.status_code == 200
        assert json.loads(result.data) == self.data['teams']

    def test_get_all_teams_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_team_data(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/teams/6')
        result_data = self.get_team_data('6')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_get_specific_team_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/6', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_team_data(self):
        self.login_user('admin', 'admin')
        query_data = {
            "name": "University of Washington, Tacoma",
            "id": "7"
        }
        result_data = {
            "name": "University of Washington, Tacoma"
        }
        post = self.app.post('/teams/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/teams/7'
        result = self.app.get('/teams/7')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_team_data_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "name": "University of Washington, Tacoma",
            "id": "7",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/teams/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/teams/7')
        assert result.status_code == 404

    def test_create_team_data_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "name": "University of Washington, Tacoma"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        result_data = self.data['teams']
        post = self.app.post('/teams/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/teams/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_team_data_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/teams/', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data

    def test_modify_team_data(self):
        self.login_user('admin', 'admin')
        query_data = {
            "name": "WWU"
        }
        result_data = {
            "name": "WWU"
        }
        patch = self.app.patch('/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_data_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "name": "WWU",
            "id": "7"
        }
        patch_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'id' is not valid for this interface."
        }
        result_data = self.get_team_data('2')
        patch = self.app.patch('/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data
        result = self.app.get('/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_data_no_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        result_data = self.get_team_data('2')
        patch = self.app.patch('/teams/2', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/teams/2')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_modify_team_data_no_data(self):
        self.login_user('admin', 'admin')
        patch_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        patch = self.app.patch('/teams/2')
        assert patch.status_code == 403
        assert json.loads(patch.data) == patch_data

    def test_delete_team_data(self):
        self.login_user('admin', 'admin')
        delete = self.app.delete('/teams/1')
        assert delete.status_code == 204
        result = self.app.get('/teams/1')
        assert result.status_code == 404

    def test_delete_team_data_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        delete_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        delete = self.app.delete('/teams/1', data=json.dumps(query_data))
        assert delete.status_code == 403
        assert json.loads(delete.data) == delete_data