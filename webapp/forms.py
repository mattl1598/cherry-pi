from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
	access_key = HiddenField("Access Key")
	firstname = StringField('Firstname', validators=[DataRequired(), Length(min=1, max=20)])
	lastname = StringField('Lastname', validators=[DataRequired(), Length(min=0, max=30)])
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
