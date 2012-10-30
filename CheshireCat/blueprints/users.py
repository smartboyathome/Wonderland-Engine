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
import bcrypt
from flask import Response, url_for, redirect, g, request, Blueprint
from flask.ext.login import login_required
from CheshireCat import app
from CheshireCat.utils import create_error_response, requires_parameters, requires_no_parameters, requires_roles, hash_password
from bson import json_util
import json

blueprint = Blueprint(__name__, 'users', url_prefix='/users')

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def get_all_users():
    data = g.db.get_all_users()
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_parameters(required=['id', 'password', 'email', 'role'], optional=['team'])
def create_user():
    data = json.loads(request.data)
    if len(g.db.get_specific_user(data['id'])) != 0:
        return create_error_response("Exists",  "A user with the id '{}' already exists".format(data['id']))
    if data['role'] in ('administrator', 'organizer', 'attacker'):
        g.db.create_user(data['id'], hash_password(data['password']), data['email'], data['role'])
        resp = redirect(url_for(".get_user", user_id=data['id']), code=201)
        return resp
    elif data['role'] == 'team':
        if 'team' not in data:
            return create_error_response('IllegalParameter', 'Users with role "team" must have the "team" parameter.')
        else:
            g.db.create_user(data['id'], hash_password(data['password']), data['email'], data['role'], team=data['team'])
            resp = redirect(url_for(".get_user", user_id=data['id']), code=201)
            return resp
    else:
        return create_error_response('InvalidRole', 'Users can only have roles "administrator", "organizer", "attacker", or "team".')

@blueprint.route("/roles/<role_id>", methods=['GET'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def get_all_users_with_role(role_id):
    data = g.db.get_all_users_with_role(role_id)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<user_id>", methods=['GET'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def get_user(user_id):
    data = g.db.get_specific_user(user_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<user_id>", methods=['PATCH'])
@login_required
@requires_roles('administrator')
@requires_parameters(optional=['password', 'email', 'role', 'team'])
def modify_user(user_id):
    data = json.loads(request.data)
    orig_data = g.db.get_specific_user(user_id)
    if len(orig_data) == 0:
        return Response(status=404)
    if 'role' in data:
        role = data['role']
    else:
        role = orig_data[0]['role']
    if role in ('administrator', 'organizer', 'attacker') and 'team' in data:
        return create_error_response('IllegalParameter', 'Only users with the "team" role can have the "team" parameter.')
    g.db.modify_user(user_id, **data)
    resp = Response(status=204)
    return resp

@blueprint.route("/<user_id>", methods=['DELETE'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def delete_user(user_id):
    data = list(g.db.get_specific_user(user_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_user(user_id)
    return Response(status=204)