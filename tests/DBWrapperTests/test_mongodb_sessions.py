from copy import deepcopy
from datetime import datetime, timedelta
from tests import show_difference_between_dicts
from tests.DBWrapperTests import DBTestCase

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