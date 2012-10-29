from flask import Response, g, Blueprint
from flask.ext.login import login_required
from CheshireCat.utils import requires_no_parameters, requires_roles, convert_all_datetime_to_timestamp
from bson import json_util
import json

blueprint = Blueprint(__name__, 'check_classes', url_prefix='/check_classes')

@blueprint.route("/", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_all_check_classes():
    data = g.db.get_all_check_classes()
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@blueprint.route("/<class_id>", methods=['GET'])
@login_required
@requires_roles('administrator', 'organizer')
@requires_no_parameters
def get_specific_check_class(class_id):
    data = g.db.get_specific_check_class(class_id)
    js = json.dumps(data, default=json_util.default)
    resp = Response(js, status=200, mimetype='application/json')
    return resp