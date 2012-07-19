# This module encapsulates everything related to selecting and loading configurations,
# creating the Flask app, and running it.
#
# We need the following run modes:
#   dev        - local, personal development server.
#   test       - used for automated testing.
#   team       - still local server, for development by team (specifically non-coder team members).
#   production - deployed on Heroku.
#
# Don't use environment variables for local configurations.
# Environment variables are annoying to set locally (global machine changes for a single project).
# Also we need to be able to run multiple servers on one machine (for dev/team).
#
# For production configuration, use whichever environment variables Heroku provides.
# But isolate this so it can be easily changed if we need to deploy somewhere else.
#
# Make production the default configuration so we never run in debug mode on the server by
# accident. 
#
# Isolate secrets and make it so they're only deployed if necessary
# (Can't really think of anything - there are secrets but they're needed in production. But
#  keep it mind.)
#
# Bundle default and per-configuration settings in clear places.
#
# Running the app also depends on the configuration. So we can't just create the app here,
# we also need to run it.
#
# If this code grows we could move it into its own module instead of __init__.

from __future__ import division, absolute_import
from flask import Flask
from configobj import ConfigObj
import os

__all__ = ['app', 'create_app', 'run_app']

# Set to None so code will fail screaming if create_app or run_app haven't been called
app = None

def create_app(_config_file=os.path.join(os.getcwd(), 'ScoringServer', 'settings.cfg')):
    # Create Flask app
    global app
    app = Flask("ScoringServer")

    # Load configuration file
    config = ConfigObj(_config_file)
    for key in config['CORE']:
        app.config[key] = config['CORE'][key]

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
