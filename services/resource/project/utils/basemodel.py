from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery as _BaseQuery
from sqlalchemy import orm

from project.exceptions import NotFound, BadRequest
from project.utils.enums import Status


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self, exp_descp=None):
        try:
            yield
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise BadRequest(exp_descp)


class BaseQuery(_BaseQuery):
    """overwrite  meth:filter_by"""
    def filter_by(self, **kwargs):
        """pass the field of 'status' to keyword"""
        if 'status' not in kwargs.keys():
            kwargs['status'] = Status.normal.value
        return super(BaseQuery, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        """
        Like :meth:`get` but aborts with 404
            if not found instead of returning ``None``."""
        rv = self.filter_by(id=ident).first()
        if rv is None:
            raise NotFound(description=description)
        return rv

    def first_or_404(self, description=None):
        """Like :meth:`first` but raise NotFound(exception)
            if not found instead of returning ``None``."""

        rv = self.filter_by(status=Status.normal.value).first()
        if rv is None:
            raise NotFound(description=description)
        return rv


db = SQLAlchemy(query_class=BaseQuery)


class BaseModel(db.Model):
    """fields that models both have"""
    __abstract__ = True  # not generate the table reality, must be inherited
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.SmallInteger, default=Status.normal.value)

    _json_fields = set()

    def __init__(self, **kwargs):
        """
        :param kwargs[symmetric_difference]: iterable
        :param kwargs: SQLAlchemy parameters
        """

        if kwargs.get('symmetric_difference') is not None:
            self.field = set(self._json_fields) ^ set(
                kwargs.get('symmetric_difference'))
        else:
            self.field = set(self._json_fields)
        super(BaseModel, self).__init__(**kwargs)

    @orm.reconstructor
    def field_property(self):
        self.field = self._json_fields

    def __getitem__(self, item):
        return getattr(self, item)

    def delete(self):
        self.status = Status.delete.value

    def keys(self):
        return self._json_fields
