from app import Student
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, RadioField
from wtforms.validators import Length, Email, EqualTo, DataRequired, regexp
from wtforms.fields.html5 import DateField

# - REGISTRATION FROM -
class Formname(FlaskForm):
    firstname = StringField('First name', validators=[Length(min=2, max=20)])
    lastname = StringField('Last name', validators=[Length(min=2, max=20)])
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20, message='Your nickname has to be between 2 and 20 characters')])
    email = StringField('Polito Email', validators=[DataRequired(), Email(), Length(min=26, max=26, message='Please use your Polito email')])
    password = PasswordField('Password', validators=[DataRequired()])
    password_con = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('REGISTER')



    def validate_name(self, name):
        stu = Student.query.filter_by(name=name.data).first()
        if stu:
            raise ValidationError('This username already exists! Please choose another one.')

    def validate_email(self, email):
        stu = Student.query.filter_by(email=email.data).first()
        if stu:
            raise ValidationError('You are already registered!')


# - LOGIN FORM -
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=26, max=26, message='Enter using your Polito email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


# - CREATE A MATCH FORM -
class MatchForm(FlaskForm):
    private_match = RadioField('Do you just want to book the field?', choices=[('privatematch', 'YES'),('publicmatch','NO')])
    date = DateField('Date and Time', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('CONFIRM')