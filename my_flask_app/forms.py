from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired
from my_flask_app.models import User,Question
from flask_login import current_user


class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  remember_me=BooleanField('Remember Me')
  submit = SubmitField('Login')

class TestForm(FlaskForm):
  radio=RadioField('Label', choices=[(  Question.option1,Question.option1),('value_two','v2')])