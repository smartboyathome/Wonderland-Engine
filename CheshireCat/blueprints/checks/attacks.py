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
from datetime import datetime

from flask import Response, g, request, redirect, url_for
from . import blueprint
from flask.ext.login import login_required
from CheshireCat.utils import requires_no_parameters, requires_roles, convert_all_datetime_to_timestamp, requires_parameters, create_error_response
from bson import json_util
import json

@blueprint.route("/attacks", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer', 'attacker')
@requires_no_parameters
def get_all_attack_checks():
    data = g.db.get_all_attacker_checks()
    convert_all_datetime_to_timestamp(data, ['timestamp', 'time_to_check'])
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/attacks/teams/<team_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer', 'attacker')
@requires_no_parameters
def get_all_attack_checks_for_team(team_id):
    data = g.db.get_all_attacker_checks_for_team(team_id)
    convert_all_datetime_to_timestamp(data, ['timestamp', 'time_to_check'])
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/attacks/teams/<team_id>", methods=['POST'])
@login_required
@requires_roles('administrator', 'attacker')
@requires_parameters(required=['id', 'description', 'machine', 'class_name'])
def create_attack_check_for_team(team_id):
    data = json.loads(request.data)
    if len(g.db.get_specific_attacker_check(data['id'], team_id)) != 0:
        return create_error_response("Exists",  "An attacker check with the id '{}' for team '{}' already exists".format(data['id'], team_id))
    g.db.create_attacker_check(data['id'], data['description'], data['machine'], team_id, data['class_name'])
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    resp = redirect(url_for(".get_specific_attack_check_for_team", team_id=team_id, check_id=data['id']), code=201)
    return resp

@blueprint.route("/attacks/<check_id>/teams/<team_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer', 'attacker')
@requires_no_parameters
def get_specific_attack_check_for_team(team_id, check_id):
    data = g.db.get_specific_attacker_check(check_id, team_id)
    if len(data) == 0:
        return Response(status=404)
    convert_all_datetime_to_timestamp(data, ['timestamp'])
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/attacks/<check_id>/teams/<team_id>", methods=['PATCH'])
@login_required
@requires_roles('administrator', 'attacker')
@requires_parameters(optional=['description', 'machine', 'class_name'])
def modify_attacker_check_for_team(team_id, check_id):
    data = json.loads(request.data)
    orig_data = g.db.get_specific_attacker_check(check_id, team_id)
    if len(orig_data) == 0:
        return Response(status=404)
    g.db.modify_attacker_check(check_id, team_id, **data)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    resp = Response(status=204)
    return resp

@blueprint.route("/attacks/<check_id>/teams/<team_id>", methods=['DELETE'])
@login_required
@requires_roles('administrator', 'attacker')
@requires_no_parameters
def delete_attacker_check_for_team(team_id, check_id):
    data = list(g.db.get_specific_attacker_check(check_id, team_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_attacker_check(check_id, team_id)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    return Response(status=204)