from flask import render_template, request, redirect, url_for, abort, flash, jsonify
from . import main
import os

# from .forms import [form_name]
from ..models import Teachers
from .. import db, photos
from flask_login import login_required, current_user
import markdown2

# General Application Data
from config import appData

@main.route('/')
@login_required
def index():
    '''
    View root page function that returns the index page 
    '''
    title = 'Ndogo Secondary School | Home'
    context = {
        'title' : title,
        'appData' : appData,
        'user' : current_user #Teachers.query.filter_by(id = current_user.id).first()
    }
    return render_template( 'dashboard.html', context = context )

@main.route('/api/all_students')
def stud_api():
    '''
    '''
    students = Teachers.query.all()
    return jsonify({ 'data' : students })

@main.route('/user/<int:id>')
@login_required
def profile(id):
    user = current_user
    title = f'{user.firstName}\'s profile.'
    context = {
        'title' : title,
        'appData' : appData,
        'user' : user
    }
    if id != user.id:
        return redirect(url_for('main.profile', id = current_user.id))
    return render_template("profile/profile.html", context = context)





# @main.route('/user/<uname>/update',methods = ['GET','POST'])
# @login_required
# def update_profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)
#     form = UpdateProfile()
#     if form.validate_on_submit():
#         user.bio = form.bio.data
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('.profile', uname = user.username ))
#     return render_template('profile/update.html', form = form, user = user )
