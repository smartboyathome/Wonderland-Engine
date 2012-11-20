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

import json
from CheshireCat.utils import convert_datetime_to_timestamp, convert_all_datetime_to_timestamp
from tests import show_difference_between_dicts
from tests.CheshireCatTests import FlaskTestCase

class TestRestTeamCheckClassesInterface(FlaskTestCase):
    def test_get_all_check_classes(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/check_classes')
        print rest_result.status_code, rest_result.data
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['check_classes']]
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        assert json_result == expected_result

    def test_get_all_check_classes_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/check_classes', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data

    def test_get_specific_check_class(self):
        self.login_user('admin', 'admin')
        rest_result = self.app.get('/check_classes/SampleServiceCheck')
        assert rest_result.status_code == 200
        expected_result = [obj for obj in self.data['check_classes'] if obj['id'] == 'SampleServiceCheck']
        for i in expected_result:
            del i['id']
        json_result = json.loads(rest_result.data)
        assert len(json_result) == len(expected_result)
        assert json_result == expected_result

    def test_get_specific_check_class_with_params(self):
        self.login_user('admin', 'admin')
        query_data = {
            "failure": "assured"
        }
        result_data = {
            "type": "IllegalParameter",
            "reason": "Parameters are not allowed for this interface."
        }
        result = self.app.get('/check_classes/SampleServiceCheck', data=json.dumps(query_data))
        print result.data
        assert result.status_code == 403
        assert json.loads(result.data) == result_data