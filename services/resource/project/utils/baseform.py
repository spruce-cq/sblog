# services/resource/project/utils/baseform.py


from flask import request
from wtforms import Form as _Form


class Form(_Form):
    """Pass 'flask.request.get_josn()' as form data"""
    def __init__(self, data=None, **kwargs):
        if data is None:
            data = request.get_json(silent=True)
        super(Form, self).__init__(data=data, **kwargs)
