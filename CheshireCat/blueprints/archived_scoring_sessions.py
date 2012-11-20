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
from flask import Response, g, Blueprint, request, redirect, url_for
from flask.ext.login import login_required
from CheshireCat.utils import requires_no_parameters, requires_roles, convert_all_datetime_to_timestamp, requires_parameters, create_error_response
from bson import json_util
import json

blueprint = Blueprint(__name__, 'archives', url_prefix='/archives')

@blueprint.route("", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_archived_scoring_sessions():
    data = g.db.get_all_archived_scoring_sessions()
    convert_all_datetime_to_timestamp(data)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_parameters(required=['id'])
def archive_current_scoring_session():
    data = json.loads(request.data)
    if len(g.db.get_specific_archived_scoring_session(data['id'])) != 0:
        return create_error_response("Exists",  "An archived scoring session with the id '{}' already exists".format(data['id']))
    g.db.archive_current_scoring_session(data['id'])
    resp = redirect(url_for(".get_specific_archived_scoring_session", session_id=data['id']), code=201)
    return resp

@blueprint.route("/<session_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_specific_archived_scoring_session(session_id):
    data = g.db.get_specific_archived_scoring_session(session_id)
    if len(data) == 0:
        return Response(status=404)
    convert_all_datetime_to_timestamp(data)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

