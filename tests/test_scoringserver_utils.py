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