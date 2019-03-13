import functools
import uuid
import os
from functools import wraps
import datetime
import random
from flask import session, request, abort, redirect, url_for, Response
from models.user import User
from utils import log
from models.token import Token


def login_required(route_function):
    @functools.wraps(route_function)
    def f():
        u = current_user()
        if u is None:
            log('游客用户')
            return redirect(url_for('index.index'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        t = Token.one(token=token)
        if token == t.token and t.user_id == u.id:
            Token.delete(t.id)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    form = {
        'token': token
    }
    t = Token.new(form, u.id)
    return t.token
