# services/resource/project/api/user/auth.py


from flask import jsonify, g
from sqlalchemy import or_

from project import bcrypt
from project.api.user.models import User
from project.api.user.forms import UserForm, LoginForm
from project.api.utils import authenticate
from project.exceptions import BadRequest, NotFound
from project.utils import paint
from project.utils.basemodel import db
from project.utils.jsonenhancer import toDict


auth_paint = paint.Paint()


@auth_paint.route('/auth/register', methods=['POST'])
def register_user():
    """User register."""
    form = UserForm()
    resp_message = 'Invalid payload.'
    if not form.validate():
        return BadRequest(resp_message)

    username = form.username.data
    email = form.email.data
    password = form.password.data
    user = User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()
    if not user:
        with db.auto_commit(resp_message):
            new_user = User(username, email, password)
            db.session.add(new_user)
        # generate auth token
        auth_token = new_user.encode_auth_token()
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token.decode()
        }
        return jsonify(response_object), 201
    else:
        return BadRequest('Sorry, that user already existing.')


@auth_paint.route('/auth/login', methods=['POST'])
def login_user():
    """User log in."""
    form = LoginForm()
    if not form.validate():
        return BadRequest('Invalid payload.')

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        auth_token = user.encode_auth_token()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'auth_token': auth_token.decode()
        }
        return jsonify(response_object), 200
    else:
        return NotFound('User does not exists, or password error.')


@auth_paint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user():
    """User log out."""
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200


@auth_paint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status():
    """Get user status which has already logged in."""
    user = User.query.filter_by(id=g.AuthInfo.uid).first()
    response_object = {
        'status': 'success',
        'data': toDict(user)
    }
    return jsonify(response_object), 200
