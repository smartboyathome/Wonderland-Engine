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

import json
from flask import g, Response, request
import os, redis
from . import app
from DBWrappers.Exceptions import BaseDBException
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from .utils import load_plugins, create_error_response

@app.before_request
def setup_database():
    config = app.config['DATABASE']
    g.db = MongoDBWrapper(config['HOST'], int(config['PORT']), config['DB_NAME'])

@app.before_request
def setup_memdb():
    config = app.config['REDIS']
    g.redis = redis.Redis(config['HOST'], int(config['PORT']), password=config['PASSWORD'])

@app.before_request
def https_only():
    if app.config['HTTPS_ONLY'] == 'True' and not request.base_url.split('://')[0] == 'https':
        return create_error_response("HttpsOnly", "This engine is configured to only be accessed through HTTPS.")

@app.teardown_request
def teardown_database(exception):
    g.db.close()

@app.teardown_request
def teardown_memdb(exception):
    g.redis.connection_pool.disconnect()

@app.errorhandler(BaseDBException)
def db_exception_handler(error):
    error_dict = {
        'type': type(error).__name__,
        'reason': str(error)
    }
    return json.dumps(error_dict), 403

@app.errorhandler(BaseException)
def general_exception_handler(error):
    error_dict = {
        'type': 'ServerError',
        'reason': 'The server encountered a problem. Please try again later.'
    }
    return json.dumps(error_dict), 500

@app.route("/")
def test_route():
    resp = Response("{'id': 'Wonderland Scoring Engine', 'version': 0.1}", 200)
    return resp

mods = load_plugins(os.path.join(os.path.dirname(__file__), 'blueprints'))
for name in mods:
    mod = mods[name]
    if hasattr(mod, 'blueprint') and hasattr(mod, 'url_prefix'):
        app.register_blueprint(mod.blueprint, url_prefix=mod.url_prefix)
