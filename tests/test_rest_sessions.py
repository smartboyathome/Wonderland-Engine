import json
from tests import FlaskTestCase

class TestRestSessions(FlaskTestCase):
    def login_user(self, username, password):
        query_data = {
            'username': username,
            'password': password
        }
        return self.app.post('/session/', data=json.dumps(query_data))

    def test_session_not_logged_in(self):
        result = self.app.get('/session/')
        assert result.status_code == 401

    def test_session_logged_in(self):
        self.login_user('admin', 'admin')
        result_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'role': 'administrator'
        }
        result = self.app.get('/session/')
        assert result.status_code == 200
        assert json.loads(result.data) == result_data

    def test_login_user(self):
        result = self.login_user('admin', 'admin')
        assert result.status_code == 201
        assert result.headers['Location'] == 'http://localhost/session/'

    def test_admin_role_not_logged_in(self):
        result = self.app.get('/session/admin_test')
        assert result.status_code == 401

    def test_admin_role_logged_in(self):
        self.login_user('admin', 'admin')
        result = self.app.get('/session/admin_test')
        assert result.status_code == 204