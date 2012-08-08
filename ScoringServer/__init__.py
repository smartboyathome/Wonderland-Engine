from __future__ import division, absolute_import
from flask import Flask
from configobj import ConfigObj
from flask_login import LoginManager
import os
from validate import Validator
from ScoringServer.itsdangerous_session import ItsdangerousSessionInterface
from ScoringServer.redis_signed_session import RedisSignedSessionInterface

__all__ = ['app', 'create_app', 'run_app']

# Set to None so code will fail screaming if create_app or run_app haven't been called
app = None
login_manager = None

def create_app(_config_file=os.path.join(os.getcwd(), 'settings.cfg')):
    # Create Flask app
    global app
    app = Flask("ScoringServer")

    # Load configuration file
    configspec = ConfigObj(os.path.join(os.getcwd(), 'configspec.cfg'), list_values=False)
    config = ConfigObj(_config_file, configspec=configspec)
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

    # Initialize ScoringServer
    # Import the views, to apply the decorators which use the global app object.
    from . import views

def run_app(**app_run_args):
    # Run the ScoringServer
    # See flask/app.py run() for the implementation of run().
    # See http://werkzeug.pocoo.org/docs/serving/ for the parameters of Werkzeug's run_simple().
    # If the debug parameter is not set, Flask does not change app.debug, which is set from
    # the DEBUG app config variable, which we've set in create_app().
    app.run(**app_run_args)