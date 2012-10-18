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

class TestRestTeamScoresInterface(FlaskTestCase):
    def test_get_scores_for_all_teams(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/teams/scores')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['team_scores']]
        print rest_result.data
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        for i in range(0, len(json_result)):
            expected_result[i]['timestamp'] = convert_datetime_to_timestamp(expected_result[i]['timestamp'])
            show_difference_between_dicts(json_result[i], expected_result[i])
        assert json_result == expected_result

    def test_get_scores_for_teams_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/scores', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_score_for_specific_team(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/teams/6/score')
        assert rest_result.status_code == 200
        json_result = json.loads(rest_result.data)
        expected_result = [obj for obj in self.data['team_scores'] if obj['team_id'] == '6'][0]
        del expected_result['team_id']
        expected_result['timestamp'] = convert_datetime_to_timestamp(expected_result['timestamp'])
        show_difference_between_dicts(json_result, expected_result)
        assert json_result == expected_result

    def test_get_score_for_specific_team_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/teams/6/score', data=json.dumps(query_data))
        assert result.status_code == 403
        assert json.loads(result.data) == result_data