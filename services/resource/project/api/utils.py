# services/resource/project/api/utils.py


from functools import wraps

from flask import request, g

from project import scope
from project.api.user.models import User
from project.exceptions import Unauthorized, Forbidden, BadRequest


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Forbidden('Invalid payload. Please log in again.')

        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            return Unauthorized(description=resp)

        user = User.query.filter_by(id=resp.uid).first()
        if not user:
            return Unauthorized()
        flag = scope.endpoint_in_scope(request.endpoint, resp.scope)
        if not flag:
            return Forbidden()
        g.AuthInfo = resp
        return f(*args, **kwargs)
    return decorated_function


def convert_to_int_for(ident, description='Invalid payload.'):
    try:
        ident = int(ident)
    except ValueError:
        return BadRequest(description)
    return ident
