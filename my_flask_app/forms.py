from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired
from my_flask_app.models import User,Question
from flask_login import current_user


class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  remember_me=BooleanField('Remember Me')
  submit = SubmitField('Login')


class QuestionForm(FlaskForm):
  question = TextAreaField('Question',validators=[DataRequired()])
  option1 = StringField('Option1',validators=[DataRequired()])
  option2 = StringField('Option2',validators=[DataRequired()])
  option3 = StringField('Option3')
  option4 = StringField('Option4')
  answer = StringField('Answer',validators=[DataRequired()])
  feedback = TextAreaField('Feedback',validators=[DataRequired()])
  submit = SubmitField('Update')


class EditForm(FlaskForm):
  question = TextAreaField('Question')
  option1 = StringField('Option1')
  option2 = StringField('Option2')
  option3 = StringField('Option3')
  option4 = StringField('Option4')
  answer = StringField('Answer')
  feedback = TextAreaField('Feedback')
  submit = SubmitField('Submit')


class FilterForm(FlaskForm):
    level=SelectField('Level',choices=[("All","All"),("Beginner","Beginner"),("Intermediate","Intermediate"),("Advanced","Advanced")])
    tag=SelectField('Tag',choices=[("All","All"),("Macro","Macro"),("Micro","Micro")])
    submit = SubmitField('Submit')