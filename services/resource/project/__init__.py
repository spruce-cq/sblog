# services/resource/project/__init__.py

import os
import click
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from project.config import config
from project.exceptions import APIException, InternalServerError
from project.utils.basemodel import db


# instantiate extensions
bcrypt = Bcrypt()
cors = CORS()


def create_app(config_name=None):

    # instantiate flask app
    app = Flask(__name__)

    # set config
    if config_name is None:
        config_name = os.getenv('APP_SETTING', 'development')
    app.config.from_object(config[config_name])

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    app.shell_context_processor(lambda: {'app': app})

    # blueprints
    register_blueprint(app)

    # error handler
    register_error_handler(app)

    return app


def register_error_handler(app):
    """When 'app.config['debug']' == True, raise build-in errors """
    @app.errorhandler(Exception)
    def handler_error(error):
        if isinstance(error, HTTPException):
            description = error.description
            code = error.code
            return APIException(description=description, code=code)
        if isinstance(error, APIException):
            return error
        else:
            if app.config['DEBUG']:
                raise error
            else:
                desp = None
                click.echo(error)
                raise error
                if hasattr(error, 'message'):
                    desp = error.message
                return InternalServerError(description=desp)


def register_blueprint(app):
    from project.api import user, blog
    app.register_blueprint(user.users_bp)
    app.register_blueprint(blog.blog_bp)
