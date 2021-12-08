# this is the file for data validation

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, PasswordField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange, length
from wtforms.validators import InputRequired, Email

# OKR form

class KeyResultForm(FlaskForm):
    dcp = StringField('dcp', validators=[InputRequired(), length(min=1, max=50)])


class ObjectiveForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), length(min=1, max=50)])

class OKRForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), length(min=1, max=50)])
    date = DateField('date', validators=[DataRequired()])
    dcp = StringField('dcp', validators=[InputRequired(), length(min=1, max=50)])
    now = IntegerField('now', validators=[InputRequired(), NumberRange(0,)])
    total = IntegerField('total', validators=[InputRequired(), NumberRange(1,)])
    step = IntegerField('step', validators=[InputRequired(), NumberRange(1,)])
    urgency = RadioField('urgency', choices=[
        ('Keter','Keter'),
        ('Euclid','Euclid'),
        ('Safe','Safe'),
        ('Neturalized','Neturalized')
    ])
    note = TextAreaField('note', validators=[length(min=0, max=500)])


# login form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), length(min=6, max=15)])
    password = PasswordField('password', validators=[InputRequired(), length(min=8, max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), length(max=50)])
    username = StringField('username', validators=[InputRequired(), length(min=6, max=15)])
    password = PasswordField('password', validators=[InputRequired(), length(min=8, max=80)])

class ChangeForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), length(min=6, max=15)])
    old_password = PasswordField('old_password', validators=[InputRequired(), length(min=8, max=80)])
    new_password = PasswordField('new_password', validators=[InputRequired(), length(min=8, max=80)])


# group form
class GroupForm(FlaskForm):
    group_name = StringField('group_name', validators=[InputRequired(), length(min=1, max=50)])
