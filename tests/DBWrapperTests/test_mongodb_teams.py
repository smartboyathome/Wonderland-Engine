from copy import deepcopy
from DBWrappers.Exceptions import DoesNotExist, Exists
from tests.DBWrapperTests import DBTestCase

class TestMongoDBTeams(DBTestCase):
    def test_get_all_teams(self):
        wrapper_result = self.db_wrapper.get_all_teams()
        expected_result = self.data['teams']
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_get_specific_team(self):
        wrapper_result = self.db_wrapper.get_specific_team('6')
        expected_result = [deepcopy(team) for team in self.data['teams'] if team['id'] == '6']
        for team in expected_result:
            del team['id']
        assert wrapper_result == expected_result

    def test_get_specific_team_nonexistant_team(self):
        wrapper_result = self.db_wrapper.get_specific_team('999')
        expected_result = []
        assert wrapper_result == expected_result

    def test_create_team(self):
        self.db_wrapper.create_team('Whatcom Community College', '3')
        wrapper_result = list(self.db.teams.find({'id': '3'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'name': 'Whatcom Community College'
        }]
        assert wrapper_result == expected_result

    def test_create_team_team_exists(self):
        with self.assertRaises(Exists):
            self.db_wrapper.create_team('University of Washington', '1')

    def test_modify_team(self):
        self.db_wrapper.modify_team('2', name='WWU')
        wrapper_result = list(self.db.teams.find({'id': '2'}, {'_id': 0, 'id': 0}))
        expected_result = [{
            'name': 'WWU'
        }]
        assert wrapper_result == expected_result

    def test_modify_team_nonexistant_team(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.modify_team('999', name='Failure')

    def test_delete_team(self):
        self.db_wrapper.delete_team('1')
        wrapper_result = list(self.db.teams.find({'id': '1'}, {'_id': 0, 'id': 0}))
        expected_result = []
        assert wrapper_result == expected_result

    def test_delete_team_nonexistant(self):
        with self.assertRaises(DoesNotExist):
            self.db_wrapper.delete_team('999')