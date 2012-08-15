from tests import DBTestCase

class TestMongoDBTeams(DBTestCase):
    def test_get_all_teams(self):
        wrapper_result = self.db_wrapper.get_all_teams()
        pure_result = list(self.db['teams'].find({}, {'_id': 0}))
        expected_result = self.data['teams']
        assert expected_result == pure_result
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result

    def test_create_team(self):
        self.db_wrapper.create_team('Whatcom Community College', '3')
        wrapper_result = self.db_wrapper.get_specific_team('3')
        expected_result = [{
            'name': 'Whatcom Community College'
        }]
        assert wrapper_result == expected_result