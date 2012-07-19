from . import FlaskTestCase
import json

class TestTeamsInterface(FlaskTestCase):
    def test_1_get_all_teams_data(self):
        result = self.app.get('/teams/')
        assert result.status_code == 200
        assert json.loads(result.data) == self.data['teams']

    def test_2_get_specific_teams_data(self):
        result = self.app.get('/teams/6')
        assert result.status_code == 200
        assert json.loads(result.data) == self.data['teams']['6']

    def test_3_create_team_data(self):
        query_data = {
            "name": "University of Washington, Tacoma",
            "id": "7"
        }
        result_data = {
            "name": "University of Washington, Tacoma",
            "score": 0
        }
        post = self.app.post('/teams/', data=json.dumps(query_data), follow_redirects=True)
        assert post.status_code == 201
        assert post.headers['Location'] == 'http://localhost/teams/7'
        result = self.app.get('/teams/7')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_4_modify_team_data(self):
        query_data = {
            "name": "UW Bothell"
        }
        result_data = {
            "name": "UW Bothell",
            "score": 0
        }
        patch = self.app.patch('/teams/6', data=json.dumps(query_data))
        assert patch.status_code == 204
        result = self.app.get('/teams/6')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_5_delete_team_data(self):
        delete = self.app.delete('/teams/1')
        assert delete.status_code == 204
        result = self.app.get('/teams/1')
        assert result.status_code == 404