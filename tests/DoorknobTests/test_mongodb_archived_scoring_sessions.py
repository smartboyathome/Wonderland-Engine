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

import collections
from copy import deepcopy
from datetime import datetime
from Doorknob.Exceptions import Exists, DoesNotExist
from tests import show_difference_between_dicts
from tests.DoorknobTests import DBTestCase

class TestMongoDBArchivedScoringSessions(DBTestCase):
    def correct_all_imprecise_times(self, wrapper_result, expected_result):
        for i in range(0, len(wrapper_result)):
            for j in wrapper_result[i]:
                if isinstance(wrapper_result[i][j], list):
                    for k in range(0, len(wrapper_result[i][j])):
                        for l in wrapper_result[i][j][k]:
                            if isinstance(wrapper_result[i][j][k][l], datetime):
                                self.correct_imprecise_time(wrapper_result[i][j][k], expected_result[i][j][k], l)
                elif isinstance(wrapper_result[i][j], dict):
                    for k in wrapper_result[i][j]:
                        if isinstance(wrapper_result[i][j][k], datetime):
                            self.correct_imprecise_time(wrapper_result[i][j], expected_result[i][j], k)

    def test_archive_current_scoring_session(self):
        self.db_wrapper.archive_current_scoring_session('TestSession')
        wrapper_result = list(self.db.archived_sessions.find({'id': 'TestSession'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'session': self.db_wrapper.get_current_scoring_session(),
            'teams': self.db_wrapper.get_all_teams(),
            'team_configs': self.db_wrapper.get_all_team_configs_for_all_machines(),
            'team_scores': self.db_wrapper.get_scores_for_all_teams(),
            'completed_checks': self.db_wrapper.get_all_completed_checks(),
            'active_checks': self.db_wrapper.get_all_checks(),
            'check_scripts': self.db_wrapper.get_all_check_scripts(),
            'check_classes': self.db_wrapper.get_all_check_classes(),
            'machines': self.db_wrapper.get_all_machines(),
            'users': self.db_wrapper.get_all_users()
        }]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_archive_current_scoring_session_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.archive_current_scoring_session('first_session')

    def test_get_all_scoring_sessions(self):
        wrapper_result = self.db_wrapper.get_all_archived_scoring_sessions()
        expected_result = self.data['archived_sessions']
        assert len(wrapper_result) == len(expected_result)
        self.correct_all_imprecise_times(wrapper_result, expected_result)
        assert wrapper_result == expected_result

    def test_get_specific_archived_scoring_session(self):
        wrapper_result = self.db_wrapper.get_specific_archived_scoring_session('first_session')
        expected_result = [deepcopy(obj) for obj in self.data['archived_sessions'] if obj['id'] == 'first_session']
        del expected_result[0]['id']
        assert len(wrapper_result) == len(expected_result)
        self.correct_all_imprecise_times(wrapper_result, expected_result)
        assert wrapper_result == expected_result

    def test_get_specific_archived_scoring_session_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_archived_scoring_session('NonexistantSession')
        expected_result = []
        assert wrapper_result == expected_result