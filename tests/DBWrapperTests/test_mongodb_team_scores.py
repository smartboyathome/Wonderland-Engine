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