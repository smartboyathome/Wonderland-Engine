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

class TestRestScoringInterface(FlaskTestCase):
    def test_get_current_scoring_session(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/scoring/')
        expected_result = self.data['session'][0]
        convert_all_datetime_to_timestamp(expected_result, ['start_time', 'end_time'])
        assert rest_result.status_code == 200
        print rest_result.data
        assert json.loads(rest_result.data) == self.data['session'][0]

    def test_get_current_scoring_session_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/scoring/', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_start_scoring_session(self):
        self.login_user('admin', 'admin')
        post = self.app.post('/scoring/')
        assert post.status_code == 204
        assert list(self.db['session'].find())[0]['state'] == 'started'

    def test_start_scoring_session_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        post = self.app.post('/scoring/', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_stop_scoring_session(self):
        self.login_user('admin', 'admin')
        post = self.app.post('/scoring/')
        assert post.status_code == 204
        assert list(self.db['session'].find())[0]['state'] == 'started'
        patch = self.app.patch('/scoring/')
        assert patch.status_code == 204
        assert list(self.db['session'].find())[0]['state'] == 'stopped'


    def test_stop_scoring_session_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        post = self.app.patch('/scoring/', data=json.dumps(query_data), follow_redirects=True)
        print post.status_code, post.data
        assert post.status_code == 403
        assert json.loads(post.data) == result_data

    def test_clear_scoring_session(self):
        self.login_user('admin', 'admin')
        before_result = self.app.get('/scoring/')
        assert before_result.status_code == 200
        delete = self.app.delete('/scoring/')
        assert delete.status_code == 204
        after_result = self.app.get('/scoring/')
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