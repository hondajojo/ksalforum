from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    username = db.Column(db.Text)
    nickname = db.Column(db.Text)
    avator = db.Column(db.Text)
    signature = db.Column(db.Text)
    location = db.Column(db.Text)
    website = db.Column(db.Text)
    company = db.Column(db.Text)
    role = db.Column(db.Integer, nullable = True)
    balance = db.Column(db.Integer, nullable = True)
    reputation = db.Column(db.Integer, nullable = True)
    self_intro = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable = True)
    updated = db.Column(db.DateTime, nullable = True)
    twitter = db.Column(db.Text)
    github = db.Column(db.Text)
    douban = db.Column(db.Text)
    last_login = db.Column(db.DateTime, nullable = True)

    def get_id(self):
        try:
            return unicode(self.uid)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    last_replied_by = db.Column(db.Text)
    status = db.Column(db.Integer, nullable = True)
    hits = db.Column(db.Integer, nullable = True, default=0)
    node_id = db.Column(db.Integer, nullable = True)
    author_id = db.Column(db.Integer, nullable = True)
    reply_count = db.Column(db.Integer, nullable = True)
    up_vote = db.Column(db.Integer, nullable = True)
    down_vote = db.Column(db.Integer, nullable = True)
    created = db.Column(db.DateTime, nullable = True)
    updated = db.Column(db.DateTime, nullable = True)
    last_replied_time = db.Column(db.DateTime, nullable = True)
    last_touched = db.Column(db.DateTime, nullable = True)

class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key = True)
    plane_id = db.Column(db.Integer, nullable = True)
    topic_count = db.Column(db.Integer, nullable = True, default=0)
    limit_reputation = db.Column(db.Integer, nullable = True)
    name = db.Column(db.Text)
    slug = db.Column(db.Text)
    thumb = db.Column(db.Text)
    introduction = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    custom_style = db.Column(db.Text)

class Plane(db.Model):
    __tablename__ = 'plane'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key = True)
    topic_id = db.Column(db.Integer, nullable = True)
    author_id = db.Column(db.Integer, nullable = True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    up_vote = db.Column(db.Integer, nullable = True)
    down_vote = db.Column(db.Integer, nullable = True)
    last_touched = db.Column(db.DateTime)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key = True)
    owner_user_id = db.Column(db.Integer, nullable = True)
    involved_type = db.Column(db.Integer, nullable = True)
    involved_topic_id = db.Column(db.Integer, nullable = True)
    involved_reply_id = db.Column(db.Integer, nullable = True)
    created = db.Column(db.DateTime)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
