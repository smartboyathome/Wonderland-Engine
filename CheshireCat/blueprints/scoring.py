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
from flask.ext.login import login_required
from CheshireCat.utils import create_error_response, requires_parameters, requires_no_parameters, requires_roles, convert_all_datetime_to_timestamp
from bson import json_util
import json

blueprint = Blueprint(__name__, 'scoring', url_prefix='/scoring')

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_scoring_session():
    data = g.db.get_current_scoring_session()
    if len(data) == 0:
        return Response(status=404)
    convert_all_datetime_to_timestamp(data, ['start_time', 'end_time'])
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def start_scoring_session():
    g.db.start_current_scoring_session()
    g.redis.publish(g.daemon_channel, 'start')
    resp = Response(status=204)
    return resp

@blueprint.route("/", methods=['PATCH'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def stop_scoring_session():
    g.db.stop_current_scoring_session()
    g.redis.publish(g.daemon_channel, 'stop')
    resp = Response(status=204)
    return resp

@blueprint.route("/", methods=['DELETE'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def clear_scoring_session():
    old_session = g.db.get_current_scoring_session()
    g.db.clear_current_scoring_session()
    if old_session[0]['state'] == 'started':
        g.redis.publish(g.daemon_channel, 'stop')
    return Response(status=204)