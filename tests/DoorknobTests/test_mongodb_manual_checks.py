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
from Doorknob.Exceptions import Exists, DoesNotExist
from tests.DoorknobTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBManualChecks(DBTestCase):
    def test_get_all_manual_checks(self):
        wrapper_result = self.db_wrapper.get_all_manual_checks()
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'manual']
        for item in expected_result:
            del item['type']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_manual_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'manual'][0]
        result_id = expected_result['id']
        team_id = expected_result['team_id']
        del expected_result['type'], expected_result['id'], expected_result['team_id']
        wrapper_result = self.db_wrapper.get_specific_manual_check(result_id, team_id)[0]
        self.correct_imprecise_time(wrapper_result, expected_result, 'timestamp')
        assert wrapper_result == expected_result

    def test_get_specific_manual_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_manual_check('UnplannedPlanningExercise', '1')
        expected_result = []
        assert wrapper_result == expected_result

    def test_get_specific_manual_check_nonexistant_for_team(self):
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['type'] == 'manual'][0]
        wrapper_result = self.db_wrapper.get_specific_manual_check(expected_result['id'], '2')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_manual_check(self):
        self.db_wrapper.create_manual_check('MobileSecurityOptions', 'The teams had to write up information on mobile security.', 'The team performed well on this task.', '114', '6', 5)
        wrapper_result = list(self.db.completed_checks.find({'id': 'MobileSecurityOptions', 'type': 'manual', 'team_id': '6'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = [{
            'description': 'The teams had to write up information on mobile security.',
            'comments': 'The team performed well on this task.',
            'inject_number': '114',
            'score': 5
        }]
        assert len(wrapper_result) == len(expected_result)
        assert wrapper_result == expected_result

    def test_create_manual_check_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_manual_check('BoardPresentation', 'The teams present to a board on what they did.', 'This team did great! They definitely deserve full points!', '107', '6', 5)

    def test_modify_manual_check(self):
        self.db_wrapper.modify_manual_check('BoardPresentation', '1', comments='They had no preparation whatsoever. They deserve to be failed.')
        wrapper_result = list(self.db.completed_checks.find({'id': 'BoardPresentation', 'type': 'manual', 'team_id': '1'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = [deepcopy(obj) for obj in self.data['completed_checks'] if obj['id'] == 'BoardPresentation' and obj['type'] == 'manual' and obj['team_id'] == '1']
        expected_result[0]['comments'] = 'They had no preparation whatsoever. They deserve to be failed.'
        del expected_result[0]['id'], expected_result[0]['type'], expected_result[0]['team_id']
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'timestamp')
        assert wrapper_result == expected_result

    def test_modify_manual_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_manual_check('UnplannedPlanningExercise', '2', description='Check whether teams completed an unplanned planning exercise.')

    def test_delete_manual_check(self):
        wrapper_result = list(self.db.completed_checks.find({'id': 'USBPolicy', 'type': 'manual', 'team_id': '1'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        assert len(wrapper_result) > 0
        self.db_wrapper.delete_manual_check('USBPolicy', '1')
        wrapper_result = list(self.db.completed_checks.find({'id': 'USBPolicy', 'type': 'manual', 'team_id': '1'}, {'_id': 0, 'id': 0, 'type': 0, 'team_id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_manual_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_manual_check('UnplannedPlanningExercise', '2')