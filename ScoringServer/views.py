from flask import g, Response
import pymongo, inspect
from ScoringServer import app

@app.before_request
def setup_database():
    config = app.config['DATABASE']
    connection = pymongo.Connection(config['HOST'], int(config['PORT']))
    g.db = connection[config['DB_NAME']]

@app.teardown_request
def teardown_database(exception):
    g.db.connection.close()

@app.route("/")
def test_route():
    resp = Response("Hello, World!", 200)
    return resp

from .plugins import teams
app.register_blueprint(teams.blueprint, url_prefix=teams.url_prefix)

'''from . import plugins
members = inspect.getmembers(plugins, predicate=inspect.ismodule)
for name, obj in members:
    if hasattr(obj, 'blueprint') and hasattr(obj, 'url_prefix'):
        app.register_blueprint(obj.blueprint, url_prefix=obj.url_prefix)'''
