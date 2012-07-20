# Taken from http://flask.pocoo.org/snippets/75/ and http://flask.pocoo.org/snippets/51/
# This is a Redis-based session interface with signed session cookies using Itsdangerous.
# Why? Because this means they can't brute force anything. ;)

import json
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature


class RedisSignedSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSignedSessionInterface(SessionInterface):
    data_serializer = json
    salt = 'cookie-session'
    session_class = RedisSignedSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def get_serializer(self, app):
        if not app.secret_key:
            return None
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt)

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        cookie_serializer = self.get_serializer(app)
        if cookie_serializer is None:
            return None
        sid_signed = request.cookies.get(app.session_cookie_name)
        try:
            if not sid_signed:
                raise BadSignature("")
            sid = cookie_serializer.loads(sid_signed, max_age=self.get_redis_expiration_time().total_seconds())
        except BadSignature:
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.data_serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                    domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.data_serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
            int(redis_exp.total_seconds()))
        sid_signed = self.get_serializer(app).dumps(session.sid)
        response.set_cookie(app.session_cookie_name, sid_signed,
            expires=cookie_exp, httponly=True,
            domain=domain)