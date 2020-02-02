from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, ValidationError, TextAreaField

from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField('Username or Email', validators=[DataRequired(), Length(min=4,max=100)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,)])
	remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(), 
		Length(min=4,max=100),
		])
	email = StringField('Email', validators=[
		DataRequired(), 
		Email(message='Invalid email adress'), 
		Length(max=100,),
		])
	password = PasswordField('Password', validators=[
		DataRequired(), 
		Length(min=8,), 
		EqualTo('confirm',message='Passwords must match'),
		])
	confirm = PasswordField('Confirm Password', validators=[DataRequired(),])
	remember = BooleanField('Remember Me')

	def create_error(message = None):
		raise ValidationError(message)

class TodoForm(FlaskForm):
	title = StringField('Title',validators=[
		DataRequired(),
		Length(min=4),
		])
	description = TextAreaField('Description', validators=[
		DataRequired(),
		Length(min=4, max=1000),
		])
	search = StringField('Search Todo')

