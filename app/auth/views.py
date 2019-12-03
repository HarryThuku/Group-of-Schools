from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import db, Teachers
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user, confirm_login
from ..email import mail_message

# General Application Data
from config import appData

@auth.route('/login', methods = ['GET','POST'])
def login():
    '''
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Teachers.query.filter_by(email = str(login_form.email.data).strip()).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, remember = login_form.remember.data, fresh = True)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid Email or Password.')

    title = "Teacher Login."
    context = {
        'title' : title,
        'appData' : appData,
        'login_form' : login_form
    }
    return render_template('auth/login.html', context = context)

@auth.route('/register', methods = ["GET", "POST"])
def register():
    '''
    
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        teacher = Teachers(
            form.firstName.data,
            form.lastName.data,
            form.surName.data,
            form.nationalID.data,
            form.email.data,
            None,
            form.tscNo.data,
            form.password.data
            )
        if teacher.create_teacher(teacher):

            # mail_message( f"CONGRATULATIONS {form.firstName.data}! You are successfully registered to {appData['institution_name']} systems!", "email/welcome_user", teacher.email, user = teacher, appData = appData)
            return redirect(url_for('auth.login'))
        return 'An Error occured! Please check your Internet connection and try again.'
    title = "Teacher Registration."
    context = {
        'title' : title,
        'appData' : appData,
        'registration_form' : form
    }
    return render_template( 'auth/registration.html', context = context )


@auth.route('/logout')
@login_required
def logout():
    '''
    '''
    logout_user()
    return redirect(url_for("auth.login"))