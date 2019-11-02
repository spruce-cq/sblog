# services/resource/project/api/usrs/users.py


from flask import jsonify

from project.api.user.models import User
from project.api.user.forms import UserForm
from project.api.utils import authenticate
from project.exceptions import BadRequest, NotFound
from project.utils.paint import Paint
from project.utils.basemodel import db
from project.utils.jsonenhancer import toDict


users_paint = Paint()


# routes
@users_paint.route('/users/ping', methods=['GET'])
def ping_pong():
    """Testing route."""
    return jsonify({
        'status': 'success',
        'message': 'pong'
    })


@users_paint.route('/users', methods=['POST'])
@authenticate
def add_user():
    """Add a new user, you must have permissions"""
    form = UserForm()
    resp_message = 'Invalid payload.'
    if not form.validate():
        return BadRequest(resp_message)

    username = form.username.data
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()
    if not user:
        with db.auto_commit(resp_message):
            user = User(username, email, password)
            db.session.add(user)
        response_object = {
            'status': 'success',
            'message': f'{email} was added'
        }
        return jsonify(response_object), 201
    else:
        return BadRequest('Sorry, the email is already existing.')


@users_paint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    resp_message = 'User does not exists.'
    try:
        user_id = int(user_id)
    except ValueError:
        return NotFound(resp_message)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return NotFound(resp_message)
    else:
        response_object = {
            'status': 'success',
            'data': toDict(user)
        }
        return jsonify(response_object), 200


@users_paint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [toDict(user) for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200
