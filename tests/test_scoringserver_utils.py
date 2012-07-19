from ScoringServer import utils
from unittest import TestCase

class TestScoringServerUtils(TestCase):
    def setUp(self):
        self.json_data = {
            "1": {
                "name": "University of Washington, Seattle",
                "score": 0
            },
            "6": {
                "name": "University of Washington, Bothell",
                "score": 0
            }
        }
        self.mongodb_data = [
            {
                "name": "University of Washington, Seattle",
                "score": 0,
                "id": "1"
            },
                {
                "name": "University of Washington, Bothell",
                "score": 0,
                "id": "6"
            }
        ]

    def test_is_compound_dict(self):
        assert utils.is_compound_dict(self.json_data)

    def test_is_mongodb_list(self):
        assert utils.is_mongodb_list(self.mongodb_data)

    def test_dict_to_mongodb_list(self):
        expected_result = self.mongodb_data
        result = utils.dict_to_mongodb_list(self.json_data)
        assert expected_result == result

    def test_mongodb_list_to_dict(self):
        expected_result = self.json_data
        result = utils.mongodb_list_to_dict(self.mongodb_data)
        assert expected_result == result