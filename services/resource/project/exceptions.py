# services/resource/project/exceptions.py


from werkzeug.exceptions import HTTPException
from flask import json


class APIException(HTTPException):
    code = None
    description = None

    def __init__(self, description=None, response=None, code=None):
        super(APIException, self).__init__(description, response)
        if code is not None:
            self.code = code

    def get_headers(self, environ=None):
        """Get a list of headers"""
        return [('content-type', 'application/json')]

    def get_body(self, environ=None):
        """ Get json formats"""
        data = {
            'code': self.code,
            'message': self.description,
            'status': 'fail'
        }
        body = json.dumps(data)
        return body


class NotFound(APIException):
    code = 404
    description = 'Not Found!'


class BadRequest(APIException):
    code = 400
    description = 'Bad Request!'


class InternalServerError(APIException):
    code = 500
    description = 'Internal Server Error!'


class Unauthorized(APIException):
    code = 401
    description = 'Provide a valid auth token.'


class Forbidden(APIException):
    code = 403
    description = "You do not have permission to do that."
