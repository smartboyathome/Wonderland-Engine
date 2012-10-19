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
from flask import Response, url_for, redirect, g, request, Blueprint
from flask.ext.login import login_required, current_user
from ScoringServer.utils import create_error_response, requires_parameters, requires_no_parameters, requires_roles
from bson import json_util
import json

blueprint = Blueprint(__name__, 'current_team', url_prefix='/current_team')

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('team')
@requires_no_parameters
def get_current_team():
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = g.db.get_specific_team(team_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/configs", methods=['GET'])
@login_required
@requires_roles('team')
@requires_no_parameters
def get_all_configs_for_current_team():
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = g.db.get_team_config_for_all_machines(team_id)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/configs", methods=['POST'])
@login_required
@requires_roles('team')
@requires_parameters(required=['machine_id'], forbidden=['team_id'], misc_allowed=True)
def create_team_config_for_machine():
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = json.loads(request.data)
    if len(g.db.get_team_config_for_machine(team_id, data['machine_id'])) != 0:
        return create_error_response("Exists",  "A config for team '{}' machine '{}' already exists".format(team_id, data['machine_id']))
    g.db.create_team_config_for_machine(team_id, **data)
    resp = redirect(url_for(".get_config_for_team", machine_id=data['machine_id']), code=201)
    return resp

@blueprint.route("/configs/<machine_id>", methods=['GET'])
@login_required
@requires_roles('team')
@requires_no_parameters
def get_config_for_team(machine_id):
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = g.db.get_team_config_for_machine(team_id, machine_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/configs/<machine_id>", methods=['PATCH'])
@login_required
@requires_roles('team')
@requires_parameters(forbidden=['team_id', 'machine_id'], misc_allowed=True)
def modify_config_for_team(machine_id):
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = json.loads(request.data)
    orig_data = g.db.get_specific_team(team_id)
    if len(orig_data) == 0:
        return Response(status=404)
    g.db.modify_team_config_for_machine(team_id, machine_id, **data)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    resp = Response(status=204)
    return resp

@blueprint.route("/configs/<machine_id>", methods=['DELETE'])
@login_required
@requires_roles('team')
@requires_no_parameters
def delete_config_for_team(machine_id):
    team_id = g.db.get_specific_user(current_user.get_id())[0]['team']
    data = list(g.db.get_team_config_for_machine(team_id, machine_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_team_config_for_machine(team_id, machine_id)
    return Response(status=204)