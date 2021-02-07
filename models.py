
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.userid')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.userid'))
                     )

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.String(80), index=True,unique=True, primary_key=True)
    username= db.Column(db.String(80), index=True)
    password = db.Column(db.String(80))
    slogan=db.Column(db.String(80))
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == userid),
                               secondaryjoin=(followers.c.followed_id == userid),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self


    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.userid).count() > 0

    def get_id(self):
        return (self.userid)


class Blogpost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.String(80))
    title=db.Column(db.String(80))
    mood=db.Column(db.String(80))
    author=db.Column(db.String(20))
    date_posted=db.Column(db.DateTime)
    content=db.Column(db.Text)


