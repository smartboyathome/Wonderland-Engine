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

from . import blueprint
from datetime import datetime
from flask.ext.login import login_required, current_user
import json
from bson import json_util
from flask.globals import request, g
from flask.helpers import url_for
from flask.wrappers import Response
from werkzeug.utils import redirect
from ScoringServer.utils import requires_no_parameters, requires_roles, requires_parameters, create_error_response, convert_datetime_to_timestamp

@blueprint.route("/scores", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_scores_for_teams():
    data = g.db.get_scores_for_all_teams()
    for item in data:
        item['timestamp'] = convert_datetime_to_timestamp(item['timestamp'])
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<team_id>/score", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_score_for_team(team_id):
    data = g.db.get_score_for_team(team_id)
    if len(data) == 0:
        return Response(status=404)
    data[0]['timestamp'] = convert_datetime_to_timestamp(data[0]['timestamp'])
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp