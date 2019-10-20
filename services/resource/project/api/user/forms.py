# services/resource/project/api/users/forms.py


from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, Length

from project.utils.baseform import Form


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(
        validators=[
            DataRequired(),
            Regexp('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9a-zA-Z]{5,16}$')])


class UserForm(LoginForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=30)])
