from tests import DBTestCase

class TestMongoDBTeams(DBTestCase):
    def test_get_all_teams(self):
        wrapper_result = self.db_wrapper.get_all_teams()
        pure_result = list(self.db['teams'].find({}, {'_id': 0}))
        expected_result = self.data['teams']
        assert not len(wrapper_result) == 0
        assert wrapper_result == expected_result