from copy import deepcopy
from tests import DBTestCase


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

    def test_get_team_configs_for_team_machine(self):
        wrapper_result = self.db_wrapper.get_team_config_for_machine('1', 'MongoDB')
        expected_result = [deepcopy(config) for config in self.data['team_configs'] if config['team_id'] == '1' and config['machine_id'] == 'MongoDB']
        for item in expected_result:
            del item['team_id'], item['machine_id']
        assert wrapper_result == expected_result

    def test_create_team_config(self):
        self.db_wrapper.create_team_config_for_machine('6', 'MongoDB', username='team3', password='team3mongo', port=63789)
        wrapper_result = list(self.db.team_configs.find({'team_id': '6', 'machine_id': 'MongoDB'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = [{
            'username': 'team3',
            'password': 'team3mongo',
            'port': 63789
        }]
        assert wrapper_result == expected_result

    def test_modify_team_config(self):
        self.db_wrapper.modify_team_config_for_machine('2', 'Redis', password='attax0r')
        wrapper_result = list(self.db.team_configs.find({'team_id': '2', 'machine_id': 'Redis'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = [{
            'username': 'team2',
            'password': 'attax0r',
            'port': 6379
        }]
        assert wrapper_result == expected_result

    def test_delete_team_config(self):
        self.db_wrapper.delete_team_config_for_machine('1', 'Apache')
        wrapper_result = list(self.db.machines.find({'team_id': '1', 'machine_id': 'Apache'}, {'_id': 0, 'team_id': 0, 'machine_id': 0}))
        expected_result = []
        assert wrapper_result == expected_result