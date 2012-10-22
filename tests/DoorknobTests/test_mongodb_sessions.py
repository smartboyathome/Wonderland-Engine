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
from datetime import datetime, timedelta
from tests import show_difference_between_dicts
from tests.DoorknobTests import DBTestCase

class TestMongoDBSessions(DBTestCase):
    def test_get_current_scoring_session(self):
        wrapper_result = self.db_wrapper.get_current_scoring_session()
        expected_result = deepcopy(self.data['session'])
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'start_time')
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'end_time')
        assert wrapper_result == expected_result

    def test_start_current_scoring_session(self):
        self.db_wrapper.start_current_scoring_session()
        wrapper_result = list(self.db.session.find({}, {'_id': 0}))
        expected_result = [{
            'start_time': wrapper_result[0]['start_time'],
            'end_time': datetime(1,1,1),
            'state': 'started'
        }]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'start_time')
        assert wrapper_result == expected_result

    def test_stop_current_scoring_session(self):
        self.db_wrapper.start_current_scoring_session()
        end_time = datetime.now()
        self.db_wrapper.stop_current_scoring_session()
        wrapper_result = list(self.db.session.find({}, {'_id': 0}))
        expected_result = [{
            'start_time': wrapper_result[0]['start_time'],
            'end_time': end_time,
            'state': 'stopped'
        }]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'start_time')
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'end_time')
            show_difference_between_dicts(wrapper_result[i], expected_result[i])
        assert wrapper_result == expected_result

    def test_clear_current_scoring_session(self):
        self.db_wrapper.clear_current_scoring_session()
        wrapper_session_result = list(self.db.session.find({}))
        expected_result = []
        assert wrapper_session_result == expected_result
        wrapper_completed_checks_result = list(self.db.completed_checks.find({}))
        assert wrapper_completed_checks_result == expected_result