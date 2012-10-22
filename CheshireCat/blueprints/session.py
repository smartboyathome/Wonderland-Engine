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
import json, bcrypt, hashlib
from flask import Blueprint, g, redirect, url_for, Response
from flask.ext.login import login_required, login_user, logout_user
from flask.globals import request
from flask_login import UserMixin, current_user
from CheshireCat import login_manager, app
from CheshireCat.utils import requires_parameters, requires_no_parameters, create_error_response, requires_roles

blueprint = Blueprint(__name__, 'session', url_prefix='/session')

def hash_password(password):
    if app.config['SERVER']['PASSWORD_HASH'] == 'bcrypt':
        return bcrypt.hashpw(password, bcrypt.gensalt(14))
    elif app.config['SERVER']['PASSWORD_HASH'] == 'md5':
        return hashlib.md5(password).hexdigest()
    return password

@login_manager.user_loader
def load_user(username):
    return User(username)

@login_manager.unauthorized_handler
def unauthenticated_request():
    return create_error_response('NotLoggedIn', 'You must log in to access this resource.', status_code=401)

@blueprint.route("/", methods=['GET'])
@login_required
@requires_no_parameters
def get_current_session_info():
    user = g.db.get_specific_user(current_user.get_id())[0]
    user['username'] = current_user.get_id()
    js = json.dumps(user)
    return Response(js, status=200, mimetype='application/json')

@blueprint.route("/", methods=['PATCH'])
@login_required
@requires_parameters(optional=['password', 'email', 'role', 'team'])
def modify_current_user():
    user = current_user.get_id()
    data = json.loads(request.data)
    data['password'] = hash_password(data['password'])
    g.db.modify_user(user, **data)
    return Response(status=204)

@blueprint.route("/", methods=['POST'])
@requires_parameters(required=['username', 'password'])
def create_new_session():
    data = json.loads(request.data)
    data['password'] = hash_password(data['password'])
    if g.db.get_specific_user(data['username'], data['password']) == []:
        return create_error_response('IncorrectLogin', 'Either the user does not exist or password is incorrect.')
    try:
        login_user(User(data['username']), remember=True)
    except BaseException, e:
        return create_error_response(type(e).__name__, e.message)
    return redirect(url_for('session.get_current_session_info'), code=201)

@blueprint.route("/", methods=['DELETE'])
def remove_current_session():
    logout_user()
    return Response(status=204)

'''
    These next four functions are used to test your permission group. If they
    return a 401 or 403 status code, then you are not allowed to access them.
    If they return a 204 status code, then you are authorized to access them.
'''

@blueprint.route('/test_admin_access', methods=['GET'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def admin_test():
    return Response(status=204)

@blueprint.route('/test_organizer_access', methods=['GET'])
@login_required
@requires_roles('organizer')
@requires_no_parameters
def organizer_test():
    return Response(status=204)

@blueprint.route('/test_team_access', methods=['GET'])
@login_required
@requires_roles('team')
@requires_no_parameters
def team_test():
    return Response(status=204)

@blueprint.route('/test_attacker_access', methods=['GET'])
@login_required
@requires_roles('attacker')
@requires_no_parameters
def attacker_test():
    return Response(status=204)


class User(UserMixin):
    def __init__(self, user):
        self._user = unicode(user)
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self._user