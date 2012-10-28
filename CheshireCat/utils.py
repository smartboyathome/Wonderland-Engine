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

from collections import defaultdict
from datetime import datetime
from functools import wraps
import json, imp, os
from flask import Response, request
from flask.globals import g
from flask_login import current_user

def convert_all_datetime_to_timestamp(obj, dt_keys):
    '''
    This function will take a list of keys which hold datetime objects, and
    recursively search a list or dictionary for those keys to convert them from
    a datetime to a floating point timestamp object. This is done in place in
    the provided list or dictionary.
    '''
    if isinstance(obj, list):
        for i in obj:
            convert_all_datetime_to_timestamp(i, dt_keys)
    elif isinstance(obj, dict):
        for i in obj:
            if i in dt_keys and isinstance(obj[i], datetime):
                obj[i] = convert_datetime_to_timestamp(obj[i])
            elif isinstance(obj[i], list) or isinstance(obj[i], dict):
                convert_all_datetime_to_timestamp(obj[i], dt_keys)

def convert_all_timestamp_to_datetime(obj, ts_keys):
    if isinstance(obj, list):
        for i in obj:
            convert_all_datetime_to_timestamp(i, ts_keys)
    elif isinstance(obj, dict):
        for i in obj:
            if i in ts_keys and isinstance(obj[i], float):
                obj[i] = convert_timestamp_to_datetime(obj[i])
            elif isinstance(obj[i], list) or isinstance(obj[i], dict):
                convert_all_datetime_to_timestamp(obj[i], ts_keys)

def convert_datetime_to_timestamp(dt):
    retval = (dt - datetime(1970, 1, 1)).total_seconds()
    retval = int(retval * 1000) / 1000.0
    return retval

def convert_timestamp_to_datetime(ts):
    return datetime.utcfromtimestamp(ts)

def load_plugins(path):
    dir_list = os.listdir(path)
    mods = {}
    for fname in dir_list:
        try:
            if os.path.isdir(os.path.join(path, fname)) and os.path.exists(os.path.join(path, fname, '__init__.py')):
                f, filename, descr = imp.find_module(fname, [path])
                mods[fname] = imp.load_module(fname, f, filename, descr)
            elif os.path.isfile(os.path.join(path, fname)):
                name, ext = os.path.splitext(fname)
                if ext == '.py' and not name == '__init__':
                    f, filename, descr = imp.find_module(name, [path])
                    mods[name] = imp.load_module(name, f, filename, descr)
        except Exception:
            continue
    return mods

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.db.get_specific_user(current_user.get_id())[0]['role'] not in roles:
                return create_error_response('InsufficientPrivileges', 'You have insufficient privileges to access this interface.', 403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def create_error_response(error_type, reason, status_code=403):
    error = {
        "type": error_type,
        "reason": reason
    }
    resp = Response(json.dumps(error), status=status_code, mimetype='application/json')
    return resp

def create_no_params_error_response():
    return create_error_response("IllegalParameter", "No parameters were specified.")

def create_params_unnecessary_error_response():
    return create_error_response("IllegalParameter", "Parameters are not allowed for this interface.")

def requires_parameters(required=[], optional=[], forbidden=[], misc_allowed=False):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if request.data == '':
                return create_no_params_error_response()
            params = Parameters(required=required, optional=optional, forbidden=forbidden, misc_allowed=misc_allowed)
            data = json.loads(request.data)
            if not params.check(data):
                return params.create_error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def requires_no_parameters(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.data != '':
            return create_params_unnecessary_error_response()
        return f(*args, **kwargs)
    return wrapped

class Parameters(object):
    def __init__(self, required=[], optional=[], forbidden=[], misc_allowed=False):
        self.required = required
        self.optional = optional
        self.forbidden = forbidden
        self.illegal = []
        self.unspecified = []
        self.misc_allowed = misc_allowed
    def check(self, param_dict):
        if not isinstance(param_dict, (dict, list)):
            return False
        required_met = defaultdict(bool)
        for param in param_dict:
            if param in self.forbidden:
                self.illegal.append(param)
            elif param in self.required:
                required_met[param] = True
            elif param not in self.optional and not self.misc_allowed:
                self.illegal.append(param)
        for param in self.required:
            if not required_met[param]:
                self.unspecified.append(param)
        return len(self.illegal) == 0 and len(self.unspecified) == 0
    def create_error_response(self):
        if len(self.illegal) == 0 and len(self.unspecified) == 0:
            return None
        reason = ""
        if len(self.illegal) > 0:
            reason += "Parameter{plural1} '{parameters}' {plural2} not valid for this interface."
            if len(self.illegal) > 1:
                reason = reason.format(plural1="s", plural2="are", parameters="', '".join(self.illegal))
            elif len(self.illegal) == 1:
                reason = reason.format(plural1="", plural2="is", parameters=self.illegal[0])
        if len(self.unspecified) > 0:
            if not reason == "":
                reason += " Additionally, required parameter{plural1} '{parameters}' {plural2} not specified."
            else:
                reason += "Required parameter{plural1} '{parameters}' {plural2} not specified."
            if len(self.unspecified) > 1:
                reason = reason.format(plural1="s", plural2="are", parameters="', '".join(self.unspecified))
            else:
                reason = reason.format(plural1="", plural2="is", parameters=self.unspecified[0])
        return create_error_response("IllegalParameter", reason)