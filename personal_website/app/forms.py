from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ScreenForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    symptom = BooleanField('Are you currently experiencing fever, nausea, or shortness of breath?')
    contact = BooleanField('Have you been in contact with anyone with COVID-19 within the last 30 days?')
    travel = BooleanField('Have you traveled outside of the state withing the last 30 days?')
    submit = SubmitField('Submit')

    def check_name(self, name):
        name = Results.query.filter_by(name=fullname.data).first()
        if name is not None:
            raise ValidationError('This person already has been screened.')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')
    