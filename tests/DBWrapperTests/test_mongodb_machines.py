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

class TestMongoDBMachines(DBTestCase):
    def test_get_all_machines(self):
        wrapper_result = self.db_wrapper.get_all_machines()
        expected_result = self.data['machines']
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_get_specific_machine(self):
        wrapper_result = self.db_wrapper.get_specific_machine('MongoDB')
        expected_result = [deepcopy(machine) for machine in self.data['machines'] if machine['id'] == 'MongoDB']
        for machine in expected_result:
            del machine['id']
        assert wrapper_result == expected_result

    def test_get_specific_machine_nonexistant_machine(self):
        wrapper_result = self.db_wrapper.get_specific_machine('DontExist')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_machine(self):
        self.db_wrapper.create_machine('Windows Server 2008', '127.0.0.4')
        wrapper_result = list(self.db.machines.find({'id': 'Windows Server 2008'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'general_ip': '127.0.0.4'
        }]
        assert wrapper_result == expected_result

    def test_create_machine_machine_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_machine('Apache', '127.5.2.78')

    def test_modify_machine(self):
        self.db_wrapper.modify_machine('Apache', general_ip='127.255.255.254')
        wrapper_result = list(self.db.machines.find({'id': 'Apache'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'general_ip': '127.255.255.254'
        }]
        assert wrapper_result == expected_result

    def test_modify_machine_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_machine('999', name='Failure')

    def test_delete_machine(self):
        self.db_wrapper.delete_machine('Redis')
        wrapper_result = list(self.db.machines.find({'id': 'Redis'}, {'_id': 0, 'id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_machine_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_machine('Failure')