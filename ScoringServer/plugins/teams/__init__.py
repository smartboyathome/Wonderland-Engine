from flask import Blueprint

blueprint = Blueprint(__name__, 'teams')
url_prefix = '/teams'

from . import teams_info