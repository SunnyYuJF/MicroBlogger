from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Blogpost, User
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

main = Blueprint('main', __name__)

# Home page
@main.route('/')
def index():
    if current_user.is_authenticated:
        posts=Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
        return render_template('main.for_user.html',posts=posts)
    else:
        posts=Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
        return render_template('main.index.html',posts=posts)

# My blog page
@main.route('/myblog')
@login_required
def myblog():
    posts=Blogpost.query.filter_by(userid=current_user.userid).all()
    user= User.query.filter_by(userid=current_user.userid).first()
    return render_template('main.myblog.html', posts = posts, name=current_user.username, user=user, num_post=len(posts) )


# Add a new post
@main.route('/add')
@login_required
def add():
    return render_template('main.add.html')


@main.route('/addpost', methods=['POST'])
@login_required
def addpost():
    title=request.form['title']
    author=current_user.username
    userid =current_user.userid
    mood=request.form['mood']
    content=request.form['content']
    post=Blogpost(title =title,  author=author,mood=mood, content=content, date_posted=datetime.now(), userid=userid)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('main.index'))


# Edit my profile
@main.route('/edit')
@login_required
def edit():
    return render_template('main.edit.html', user=current_user)

@main.route('/editprofile', methods=['POST'])
@login_required
def editprofile():
    username=request.form['username']
    slogan=request.form['slogan']
    password=request.form['password']
    confirm=request.form['passwordvalid']
    if username:
        current_user.username=username
    if slogan:
        current_user.slogan=slogan
    if password:
        if password==confirm:
            current_user.password=password
        else:
            flash('Your passwords don not match. Please check.')
            return redirect(url_for('main.edit'))
    current_db_sessions = db.session.object_session(current_user)
    current_db_sessions.add(current_user)
    current_db_sessions.commit()
    return redirect(url_for('main.myblog'))


# Look up other's profile
@main.route('/profile/<userid>')
def profile(userid):
    posts=Blogpost.query.filter_by(userid=userid).all()
    user= User.query.filter_by(userid=userid).first()
    if current_user.is_authenticated:
        if current_user.userid==userid:
            return redirect(url_for('main.myblog'))
        else:
            return render_template('profile_for_user.html', posts = posts, user=user, num_post=len(posts))
    else:
        return render_template('profile.html', posts = posts, user=user, num_post=len(posts))


# Look up other's post
@main.route('/post/<int:post_id>')
def post(post_id):
    post=Blogpost.query.filter_by(id=post_id).one()
    if current_user.is_authenticated:
        return render_template('post_for_user.html', post = post)
    else:
        return render_template('main.post.html', post = post)



# Follow other user
@main.route('/follow/<userid>')
@login_required
def follow(userid):
    user = User.query.filter_by(userid=userid).first()
    if user is None:
        flash('User @%s not found.' % userid)
        return redirect(url_for('main.index'))
    if userid == current_user.userid:
        flash('You can\'t follow yourself!')
        return redirect(url_for('main.profile', userid=userid))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow @' + userid + '.')
        return redirect(url_for('main.profile', userid=userid))
    current_db_sessions = db.session.object_session(current_user)
    current_db_sessions.add(current_user)
    current_db_sessions.commit()
    flash('You are now following @' + userid + '!')
    return redirect(url_for('main.profile', userid=userid))

# Unfollow other user
@main.route('/unfollow/<userid>')
@login_required
def unfollow(userid):
    user = User.query.filter_by(userid=userid).first()
    if user is None:
        flash('User @%s not found.' % userid)
        return redirect(url_for('main.index'))
    if userid == current_user.userid:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('main.profile', userid=userid))
    u = current_user.unfollow(user)
    if u is None:
        flash('Cannot unfollow @' + userid + '.')
        return redirect(url_for('main.profile', userid=userid))
    current_db_sessions = db.session.object_session(current_user)
    current_db_sessions.add(current_user)
    current_db_sessions.commit()
    flash('You have stopped following @' + userid + '.')
    return redirect(url_for('main.profile', userid=userid))


