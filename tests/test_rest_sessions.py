import json
from tests import FlaskTestCase

class TestRestSessions(FlaskTestCase):
    def test_login_user(self):
        result = self.app.get('/session/')
        assert result.status_code == 401
        query_data = {
            'username': 'admin',
            'password': 'admin'
        }
        result = self.app.post('/session/', data=json.dumps(query_data))
        assert result.status_code == 201
        assert result.headers['Location'] == 'http://localhost/session/'
        result_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'role': 'administrator'
        }
        result = self.app.get('/session/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data