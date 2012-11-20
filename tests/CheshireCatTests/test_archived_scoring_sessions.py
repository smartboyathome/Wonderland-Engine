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

class TestRestArchivedScoringSessionsInterface(FlaskTestCase):
    def test_get_all_archived_scoring_sessions(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/archives')
        expected_result = self.data['archived_sessions']
        convert_all_datetime_to_timestamp(expected_result)
        assert result.status_code == 200
        assert json.loads(result.data) == expected_result

    def test_get_all_archived_scoring_sessions_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/archives', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_archived_scoring_session(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/archives/first_session')
        assert result.status_code == 200
        result_data = [obj for obj in self.data['archived_sessions'] if obj['id'] == 'first_session'][0]
        del result_data['id']
        convert_all_datetime_to_timestamp(result_data)
        json_result = json.loads(result.data)
        assert json_result == result_data

    def test_get_specific_archived_scoring_session_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/archives/MongoDB', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_create_archived_scoring_session(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "second_session"
        }
        result_data = [obj for obj in self.data['archived_sessions'] if obj['id'] == 'first_session'][0]
        del result_data['id']
        convert_all_datetime_to_timestamp(result_data)
        post = self.app.post('/archives', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/archives/second_session'
        result = self.app.get('/archives/second_session')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_archived_scoring_session_exists(self):
        self.login_user('admin', 'admin')
        query_data = {
            'id': 'first_session'
        }
        result_data = {
            "type": "Exists",
            "reason": "An archived scoring session with the id 'first_session' already exists"
        }
        post = self.app.post('/archives', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_create_archived_scoring_session_invalid_param(self):
        self.login_user('admin', 'admin')
        query_data = {
            "id": "second_session",
            "failure": "assured"
        }
        post_data = {
            "type": "IllegalParameter",
            "reason": "Parameter 'failure' is not valid for this interface."
        }
        post = self.app.post('/archives', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/archives/Dovecot')
        assert result.status_code == 404

    def test_create_archived_scoring_session_missing_param(self):
        self.login_user('admin', 'admin')
        query_data = {}
        post_data = {
            "type": "IllegalParameter",
            "reason": "Required parameter 'id' is not specified."
        }
        result_data = self.data['archived_sessions']
        for i in result_data:
            convert_all_datetime_to_timestamp(i)
        post = self.app.post('/archives', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data
        result = self.app.get('/archives')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_create_archived_scoring_session_no_data(self):
        self.login_user('admin', 'admin')
        post_data = {
            "type": "IllegalParameter",
            "reason": "No parameters were specified."
        }
        post = self.app.post('/archives', follow_redirects=True)
        assert post.status_code == 403
        assert json.loads(post.data) == post_data