
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    userid = request.form.get('userid')
    password = request.form.get('password')
    user = User.query.filter_by(userid=userid).first()

    # check if user actually exists
    if not user or user.password!=password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    userid = request.form.get('userid')
    username = request.form.get('username')
    slogan=request.form.get('slogan')
    password = request.form.get('password')
    confirm = request.form.get('passwordvalid')

    #check if wrong password
    if password != confirm:
        flash('Passwords do not match. Please Check','warning')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(userid=userid).first()

    #check if username exists
    if user:
        flash('User ID already exists','warning')
        return redirect(url_for('auth.signup'))

    # create new user
    new_user = User(username=username, password=password, slogan=slogan, userid=userid)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
