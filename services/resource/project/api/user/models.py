# services/resource/porject/api/users/models.py


import datetime
from collections import namedtuple

from flask import current_app
import jwt

from project import bcrypt
from project.utils.basemodel import BaseModel, db
from project.utils.enums import Scope


# model
class User(BaseModel):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    _json_fields = ('id', 'username', 'email', 'admin')

    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        super().__init__(**kwargs)

    def __repr__(self):
        return f'user: {self.username}'

    def encode_auth_token(self):
        """Generates the auth token."""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': {'uid': self.id, 'admin': self.admin}
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode the auth token - :param auth_token: - :return: namedtuple|string
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            AuthInfo = namedtuple('AuthInfo', ['uid', 'scope'])
            scope = Scope.admin.value if payload['sub']['admin'] else Scope.user.value
            return AuthInfo(
                payload['sub']['uid'],
                scope
            )
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
