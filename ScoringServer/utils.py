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
from functools import wraps
import json, imp, os
from flask import Response, request
from flask.globals import g
from flask_login import current_user

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

def requires_parameters(required=[], optional=[]):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if request.data == '':
                return create_no_params_error_response()
            params = Parameters(required=required, optional=optional)
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
    def __init__(self, required=[], optional=[]):
        self.required = required
        self.optional = optional
        self.illegal = []
        self.unspecified = []
    def check(self, param_dict):
        if not isinstance(param_dict, (dict, list)):
            return False
        required_met = defaultdict(bool)
        for param in param_dict:
            if param in self.required:
                required_met[param] = True
            elif param not in self.optional:
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