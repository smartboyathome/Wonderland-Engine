from . import blueprint
from flask.ext.login import login_required, current_user
import json
from bson import json_util
from flask.globals import request, g
from flask.helpers import url_for
from flask.wrappers import Response
from werkzeug.utils import redirect
from ScoringServer.utils import requires_no_parameters, requires_roles, requires_parameters, create_error_response

@blueprint.route("/<team_id>/configs", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_configs_for_team(team_id):
    data = g.db.get_team_config_for_all_machines(team_id)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<team_id>/configs", methods=['POST'])
@login_required
@requires_roles('administrator')
@requires_parameters(required=['machine_id'], forbidden=['team_id'], misc_allowed=True)
def create_team_config_for_machine(team_id):
    data = json.loads(request.data)
    if len(g.db.get_team_config_for_machine(team_id, data['machine_id'])) != 0:
        return create_error_response("Exists",  "A config for team '{}' machine '{}' already exists".format(team_id, data['machine_id']))
    g.db.create_team_config_for_machine(team_id, **data)
    resp = redirect(url_for(".get_config_for_team", team_id=team_id, machine_id=data['machine_id']), code=201)
    return resp

@blueprint.route("/<team_id>/configs/<machine_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_config_for_team(team_id, machine_id):
    data = g.db.get_team_config_for_machine(team_id, machine_id)
    if len(data) == 0:
        return Response(status=404)
    js = json.dumps(data[0], default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<team_id>/configs/<machine_id>", methods=['PATCH'])
@login_required
@requires_roles('administrator')
@requires_parameters(forbidden=['team_id', 'machine_id'], misc_allowed=True)
def modify_config_for_team(team_id, machine_id):
    data = json.loads(request.data)
    orig_data = g.db.get_specific_team(team_id)
    if len(orig_data) == 0:
        return Response(status=404)
    g.db.modify_team_config_for_machine(team_id, machine_id, **data)
    g.redis.publish(g.daemon_channel, 'changed team {}'.format(team_id))
    resp = Response(status=204)
    return resp

@blueprint.route("/<team_id>/configs/<machine_id>", methods=['DELETE'])
@login_required
@requires_roles('administrator')
@requires_no_parameters
def delete_config_for_team(team_id, machine_id):
    data = list(g.db.get_team_config_for_machine(team_id, machine_id))
    if len(data) == 0:
        return Response(status=404)
    g.db.delete_team_config_for_machine(team_id, machine_id)
    return Response(status=204)