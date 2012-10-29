from flask import Response, g, Blueprint
from flask.ext.login import login_required
from CheshireCat.utils import requires_no_parameters, requires_roles, convert_all_datetime_to_timestamp
from bson import json_util
import json

blueprint = Blueprint(__name__, 'check_scripts', url_prefix='/check_scripts')

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_check_scripts():
    data = g.db.get_all_check_scripts()
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<script_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_specific_check_script(script_id):
    data = g.db.get_specific_check_script(script_id)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp