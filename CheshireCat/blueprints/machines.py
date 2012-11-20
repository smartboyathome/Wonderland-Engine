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
from CheshireCat.utils import create_error_response, requires_parameters, requires_no_parameters, requires_roles
from bson import json_util
import json

blueprint = Blueprint(__name__, 'machines', url_prefix='/machines')

@blueprint.route("", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_machines():
    data = g.db.get_all_machines()
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_parameters(required=['id', 'general_ip'])
def create_machine():
    data = json.loads(request.data)
    if len(g.db.get_specific_machine(data['id'])) != 0:
        return create_error_response("Exists",  "A machine with the id '{}' already exists".format(data['id']))
    g.db.create_machine(data['id'], data['general_ip'])
    resp = redirect(url_for(".get_machine", machine_id=data['id']), code=201)
    return resp

@blueprint.route("/<machine_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_machine(machine_id):
    data = g.db.get_specific_machine(machine_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<machine_id>", methods=['PATCH'])
@login_required
@requires_roles('administrator')
@requires_parameters(optional=['general_ip'])
def modify_machine(machine_id):
    data = json.loads(request.data)
    orig_data = g.db.get_specific_machine(machine_id)
    if len(orig_data) == 0:
        return Response(status=404)
    g.db.modify_machine(machine_id, **data)
    resp = Response(status=204)
    return resp

@blueprint.route("/<machine_id>", methods=['DELETE'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def delete_machine(machine_id):
    data = list(g.db.get_specific_machine(machine_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_machine(machine_id)
    return Response(status=204)