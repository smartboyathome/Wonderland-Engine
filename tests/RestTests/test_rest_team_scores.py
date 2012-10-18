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