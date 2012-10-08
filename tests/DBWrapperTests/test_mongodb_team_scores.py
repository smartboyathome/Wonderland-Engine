from copy import deepcopy
from datetime import datetime
from DBWrappers.Exceptions import DoesNotExist, Exists
from tests import show_difference_between_dicts
from tests.DBWrapperTests import DBTestCase

class TestMongoDBTeamScores(DBTestCase):
    def test_get_scores_for_all_teams(self):
        wrapper_result = self.db_wrapper.get_scores_for_all_teams()
        expected_result = self.data['team_scores']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_score_for_team(self):
        wrapper_result = self.db_wrapper.get_score_for_team('6')
        expected_result = [deepcopy(team) for team in self.data['team_scores'] if team['team_id'] == '6']
        for team in expected_result:
            del team['team_id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_score_for_team_nonexistant_team(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.get_score_for_team('999')

    def test_calculate_scores_for_team(self):
        result = self.db_wrapper.calculate_scores_for_team('6')
        wrapper_result = list(self.db.team_scores.find({'team_id': '6'}, {'_id': 0, 'team_id': 0}))
        expected_result = [{
            'score': 15,
            'timestamp': result['timestamp']
        }]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_calculate_scores_for_team_nonexistant_team(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.calculate_scores_for_team('999')