from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import *
from ..models import Teachers
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField( 'Email Address', validators = [Required(), Email()] )
    password = PasswordField( 'Password', validators = [Required()] )
    remember = BooleanField('Stay Loged In?')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators = [Required()])
    lastName = StringField('Last Name', validators = [Required()])
    surName = StringField('Sur Name')
    email = StringField( 'Email Address', validators = [Required(), Email()] )
    nationalID = IntegerField( 'National ID', validators = [Required()] )
    tscNo = IntegerField('TSC Number', validators = [Required()])
    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirm', message = 'Passwords must match!')])
    password_confirm = PasswordField('Confirm Password', validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self, data_field):
        if Teachers.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an account with that email.')

    def validate_nationalId(self, data_field):
        if Teachers.query.filter_by(nationalId = data_field.data).first():
            raise ValidationError('There is an account with that National ID.')

    def validate_tscNo(self, data_field):
        if Teachers.query.filter_by(TSC_No = data_field.data).first():
            raise ValidationError('There is an account with that TSC number.')