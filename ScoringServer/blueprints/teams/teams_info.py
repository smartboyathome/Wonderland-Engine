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

from flask import Response, url_for, redirect, g, request
from . import blueprint
from flask.ext.login import login_required
from ScoringServer.utils import create_error_response, requires_parameters, requires_no_parameters, requires_roles
from bson import json_util
import json

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_teams():
    data = g.db.get_all_teams()
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_parameters(required=['name', 'id'])
def create_team():
    data = json.loads(request.data)
    if len(g.db.get_specific_team(data['id'])) != 0:
        return create_error_response("TeamExists",  "A team with the id '{}' already exists".format(data['id']))
    g.db.create_team(data['name'], data['id'])
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(data['id']))
    resp = redirect(url_for(".get_team", team_id=data['id']), code=201)
    return resp

@blueprint.route("/<team_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_team(team_id):
    data = g.db.get_specific_team(team_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<team_id>", methods=['PATCH'])
@login_required
@requires_roles('administrator')
@requires_parameters(optional=['name'])
def modify_team(team_id):
    data = json.loads(request.data)
    orig_data = g.db.get_specific_team(team_id)
    if len(orig_data) == 0:
        return Response(status=404)
    g.db.modify_team(team_id, **data)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    resp = Response(status=204)
    return resp

@blueprint.route("/<team_id>", methods=['DELETE'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def delete_team(team_id):
    data = list(g.db.get_specific_team(team_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_team(team_id)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    return Response(status=204)