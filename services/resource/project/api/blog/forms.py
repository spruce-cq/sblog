# services/resource/project/api/blog/forms.py


from wtforms import StringField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import Length, DataRequired, Optional

from project.utils.baseform import Form
from project.api.blog.models import Category


class CategoryForm(Form):
    name = StringField(validators=[DataRequired(), Length(1, 15)])


class ArticleForm(Form):
    aid = IntegerField(validators=[Optional()])
    title = StringField(validators=[DataRequired(), Length(2, 128)])
    body = TextAreaField(validators=[DataRequired()])
    category = IntegerField(validators=[DataRequired()], default=1)

    def validate_category(self, field):
        category = Category.query.get(field.data)
        if not category:
            raise ValidationError('Not found the article.')
