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
from DBWrappers.Exceptions import Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase
from .. import show_difference_between_dicts

class TestMongoDBGeneralChecks(DBTestCase):
    def test_get_all_checks(self):
        wrapper_result = self.db_wrapper.get_all_checks()
        expected_result = [deepcopy(obj) for obj in self.data['active_checks']]
        assert len(wrapper_result) == len(expected_result)
        for i in range(0, len(wrapper_result)):
            #show_difference_between_dicts(wrapper_result[i], expected_result[i])
            if 'time_to_check' in wrapper_result[i] and 'time_to_check' in expected_result[i]:
                self.correct_imprecise_time(wrapper_result[i], expected_result[i], 'time_to_check')
        assert wrapper_result == expected_result

    def test_get_specific_check(self):
        expected_result = [deepcopy(obj) for obj in self.data['active_checks']][0]
        result_id = expected_result['id']
        result_type = expected_result['type']
        del expected_result['type'], expected_result['id']
        wrapper_result = self.db_wrapper.get_specific_check(result_id, result_type)[0]
        assert wrapper_result == expected_result

    def test_get_specific_check_nonexistant(self):
        wrapper_result = self.db_wrapper.get_specific_check('NonexistantCheck', 'any')
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_check(self):
        self.db_wrapper.delete_specific_check('BrokenExploit', 'attacker')
        wrapper_result = list(self.db.active_checks.find({'id': 'BrokenExploit', 'type': 'attacker'}, {'_id': 0, 'id': 0, 'type': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_check_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_specific_check('NonexistantServiceCheck', 'service')