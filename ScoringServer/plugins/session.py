from flask import Blueprint, g, redirect, url_for, Response
from flask.ext.login import login_required, login_user, logout_user
from ScoringServer import login_manager

blueprint = Blueprint(__name__, 'session')
url_prefix = '/session'

@login_manager.user_loader
def load_user(username):
    return g.db.users.find({"username": username})

@blueprint.route("/", methods=['GET'])
@login_required
def get_current_session_info():
    return Response(status=204)

@blueprint.route("/", methods=['POST'])
def create_new_session():
    login_user(username)
    return redirect(url_for('session.get_current_session_info'))

@blueprint.route("/", methods=['DELETE'])
def remove_current_session():
    logout_user()
    return Response(status=204)