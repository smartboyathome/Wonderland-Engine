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

class TestRestSessions(FlaskTestCase):

    def test_session_not_logged_in(self):
        result = self.app.get('/session/')
        assert result.status_code == 401

    def test_session_logged_in(self):
        self.login_user('admin', 'admin')
        result_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'role': 'administrator'
        }
        result = self.app.get('/session/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_login_user(self):
        result = self.login_user('admin', 'admin')
        assert result.status_code == 201
        assert result.headers['Location'] == 'http://localhost/session/'

    def test_logout_user(self):
        self.login_user('admin', 'admin')
        result = self.app.delete('/session/')
        assert result.status_code == 204

    def test_modify_current_user(self):
        self.login_user('evil_red_team', 'evil_red_team')
        query_data = {
            'password': 'red_team_sucks',
            'email': 'team999@example.com'
        }
        result = self.app.patch('/session/', data=json.dumps(query_data))
        assert result.status_code == 204
        self.app.delete('/session/')
        result = self.login_user('evil_red_team', 'red_team_sucks')
        assert result.status_code == 201

    def test_admin_role_not_logged_in(self):
        result = self.app.get('/session/test_admin_access')
        assert result.status_code == 401

    def test_admin_role_logged_in(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/session/test_admin_access')
        assert result.status_code == 204

    def test_admin_role_insufficient_privileges(self):
        self.login_user('evil_red_team', 'evil_red_team')
        result = self.app.get('/session/test_admin_access')
        assert result.status_code == 403

    def test_organizer_role_not_logged_in(self):
        result = self.app.get('/session/test_organizer_access')
        assert result.status_code == 401

    def test_organizer_role_logged_in(self):
        self.login_user('white_team', 'white_team')
        result = self.app.get('/session/test_organizer_access')
        assert result.status_code == 204

    def test_organizer_role_insufficient_privileges(self):
        self.login_user('evil_red_team', 'evil_red_team')
        result = self.app.get('/session/test_organizer_access')
        assert result.status_code == 403

    def test_attacker_role_not_logged_in(self):
        result = self.app.get('/session/test_attacker_access')
        assert result.status_code == 401

    def test_attacker_role_logged_in(self):
        self.login_user('evil_red_team', 'evil_red_team')
        result = self.app.get('/session/test_attacker_access')
        assert result.status_code == 204

    def test_attacker_role_insufficient_privileges(self):
        self.login_user('team1', 'uw seattle')
        result = self.app.get('/session/test_attacker_access')
        assert result.status_code == 403

    def test_team_role_not_logged_in(self):
        result = self.app.get('/session/test_team_access')
        assert result.status_code == 401

    def test_team_role_logged_in(self):
        self.login_user('team1', 'uw seattle')
        result = self.app.get('/session/test_team_access')
        assert result.status_code == 204

    def test_team_role_insufficient_privileges(self):
        self.login_user('evil_red_team', 'evil_red_team')
        result = self.app.get('/session/test_team_access')
        assert result.status_code == 403