from copy import deepcopy
from DBWrappers.Exceptions import TeamDoesNotExist, MachineDoesNotExist, Exists, DoesNotExist
from tests.DBWrapperTests import DBTestCase


class TestMongoDBTeamConfigs(DBTestCase):
    def test_get_all_team_configs(self):
        wrapper_result = self.db_wrapper.get_all_team_configs_for_all_machines()
        expected_result = self.data['team_configs']
        assert wrapper_result == expected_result

    def test_get_team_configs_for_team(self):
        wrapper_result = self.db_wrapper.get_team_config_for_all_machines('1')
        expected_result = [deepcopy(config) for config in self.data['team_configs'] if config['team_id'] == '1']
        for item in expected_result:
            del item['team_id']
        assert wrapper_result == expected_result

    def test_get_team_configs_for_nonexistant_team(self):
        with self.assertRaises(TeamDoesNotExist):
            self.db_wrapper.get_team_config_for_all_machines('999')

    def test_get_team_configs_for_team_none_for_team(self):
        wrapper_result = self.db_wrapper.get_team_config_for_all_machines('6')
        expected_result = []
        assert wrapper_result == expected_result

    def test_get_team_configs_for_team_machine(self):
        wrapper_result = self.db_wrapper.get_team_config_for_machine('2', 'Redis')
        expected_result = [deepcopy(config) for config in self.data['team_configs'] if config['team_id'] == '2' and config['machine_id'] == 'Redis']
        for item in expected_result:
            del item['team_id'], item['machine_id']
        assert wrapper_result == expected_result

    def test_get_team_configs_for_team_none_for_machine(self):
        wrapper_result = self.db_wrapper.get_team_config_for_machine('6', 'Apache')
        expected_result = []
        assert wrapper_result == expected_result

    def test_get_team_configs_for_team_machine_nonexistant(self):
        with self.assertRaises(MachineDoesNotExist):
            self.db_wrapper.get_team_config_for_machine('6', 'FAILURE')

    def test_create_team_config(self):
        self.db_wrapper.create_team_config_for_machine('6', 'MongoDB', username='team3', password='team3mongo', port=63789)
        wrapper_result = list(self.db.team_configs.find({'team_id': '6', 'machine_id': 'MongoDB'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = [{
            'username': 'team3',
            'password': 'team3mongo',
            'port': 63789
        }]
        assert wrapper_result == expected_result

    def test_create_team_config_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_team_config_for_machine('1', 'MongoDB', username='team01', password='team01mongo', port=63789)

    def test_modify_team_config(self):
        self.db_wrapper.modify_team_config_for_machine('2', 'Redis', password='attax0r')
        wrapper_result = list(self.db.team_configs.find({'team_id': '2', 'machine_id': 'Redis'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = [{
            'username': 'team2',
            'password': 'attax0r',
            'port': 6379
        }]
        assert wrapper_result == expected_result

    def test_modify_team_config_team_nonexistant(self):
        with self.assertRaises(TeamDoesNotExist):
            self.db_wrapper.modify_team_config_for_machine('999', 'MongoDB', username='team999', password='team999mongo', port=63789)

    def test_modify_team_config_machine_nonexistant(self):
        with self.assertRaises(MachineDoesNotExist):
            self.db_wrapper.modify_team_config_for_machine('1', 'FAILURE', username='team1', password='team1FAILURE', port=63789)

    def test_modify_team_config_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_team_config_for_machine('2', 'Apache', username='team02', password='team02apache', port=63789)

    def test_delete_team_config(self):
        self.db_wrapper.delete_team_config_for_machine('1', 'Apache')
        wrapper_result = list(self.db.machines.find({'team_id': '1', 'machine_id': 'Apache'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_team_config_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_team_config_for_machine('6', 'MongoDB')