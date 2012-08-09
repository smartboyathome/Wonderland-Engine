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

from flask import Blueprint, g, redirect, url_for, Response
from flask.ext.login import login_required, login_user, logout_user
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringServer import login_manager

blueprint = Blueprint(__name__, 'session')
url_prefix = '/session'

@login_manager.user_loader
def load_user(username):
    return g.db.get_specific_user(username)

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