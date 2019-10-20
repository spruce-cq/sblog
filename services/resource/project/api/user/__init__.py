# services/resource/project/api/users/__init__.py


from flask import Blueprint

from project.api.user import users, auth


users_bp = Blueprint('users', __name__)
users.users_paint.depict(users_bp)
auth.auth_paint.depict(users_bp)
