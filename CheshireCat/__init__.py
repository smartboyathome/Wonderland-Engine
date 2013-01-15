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

from __future__ import division, absolute_import
from flask import Flask
from configobj import ConfigObj
from flask_login import LoginManager
import os
from validate import Validator
from CheshireCat.utils import hash_password, get_root_dir, get_first_file_that_exists
from Doorknob.MongoDBWrapper import MongoDBWrapper

__all__ = ['app', 'create_app', 'run_app']

# Set to None so code will fail screaming if create_app or run_app haven't been called
app = None
login_manager = None

default_config_dirs = [
    os.path.join(get_root_dir(), "etc", "wonderland-engine")
]

def create_app(_config_dir=None, _config_filename='settings.cfg', _configspec_filename='configspec.cfg'):
    # Create Flask app
    global app
    app = Flask("CheshireCat")

    if _config_dir is not None:
        default_config_dirs.insert(0, _config_dir)

    configspec_path = get_first_file_that_exists(default_config_dirs, _configspec_filename)
    config_path = get_first_file_that_exists(default_config_dirs, _config_filename)

    print configspec_path, config_path

    # Load configuration file
    configspec = ConfigObj(configspec_path, list_values=False)
    config = ConfigObj(config_path, configspec=configspec)
    test = config.validate(Validator(), copy=True)
    for key in config['CORE']:
        app.config[key] = config['CORE'][key]

    # Change the session interface to be more secure and portalble than the default
    # which is provided by Werkzeug.
    # These break the engine currently. I don't know why.
    #app.session_interface = RedisSignedSessionInterface()
    #app.session_interface = ItsdangerousSessionInterface()

    # Flask-Login manages user sessions for us, but we need to set it up first, so
    # we'll do so here.
    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Initialize our database
    dbconfig = config['CORE']['DATABASE']
    db = MongoDBWrapper(dbconfig['HOST'], int(dbconfig['PORT']), dbconfig['DB_NAME'])
    db.init_db()
    if len(db.get_all_users_with_role('administrator')) == 0:
        db.create_user('admin', hash_password('admin'), 'admin@example.com', 'administrator')

    # Initialize CheshireCat
    # Import the views, to apply the decorators which use the global app object.
    from . import views

def run_app(**app_run_args):
    # Run the CheshireCat
    # See flask/app.py run() for the implementation of run().
    # See http://werkzeug.pocoo.org/docs/serving/ for the parameters of Werkzeug's run_simple().
    # If the debug parameter is not set, Flask does not change app.debug, which is set from
    # the DEBUG app config variable, which we've set in create_app().
    app.run(**app_run_args)