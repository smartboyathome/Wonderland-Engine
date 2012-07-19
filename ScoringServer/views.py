from flask import g, Response
import pymongo, os, imp
from . import app
from .utils import load_plugins

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

mods = load_plugins(os.path.join(os.path.dirname(__file__), 'plugins'))
for name in mods:
    mod = mods[name]
    if hasattr(mod, 'blueprint') and hasattr(mod, 'url_prefix'):
        app.register_blueprint(mod.blueprint, url_prefix=mod.url_prefix)


'''from .plugins import teams
app.register_blueprint(teams.blueprint, url_prefix=teams.url_prefix)'''

'''from . import plugins
members = inspect.getmembers(plugins, predicate=inspect.ismodule)
for name, obj in members:
    if hasattr(obj, 'blueprint') and hasattr(obj, 'url_prefix'):
        app.register_blueprint(obj.blueprint, url_prefix=obj.url_prefix)'''
