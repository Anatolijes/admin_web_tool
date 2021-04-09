from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from src.models import User


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=5, max=150)])
    content = StringField('content', validators=[DataRequired(), Length(min=5, max=7000)])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('submit')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField("Password", validators=[
        DataRequired(message="Please Fill This Field"), EqualTo(fieldname="confirm", message=" Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(message="Fill the field")])
    submit = SubmitField('submit')

