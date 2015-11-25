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

    @classmethod
    def get_all_topics(cls):
        topics = cls.query.join(Node, cls.node_id==Node.id) \
            .join(User, cls.author_id==User.uid) \
            .order_by(cls.created.desc()) \
            .add_columns(User.username,User.avator,Node.slug,Node.name)
        return topics

    @classmethod
    def get_topics_by_node(cls, node_id=None):
        topics = cls.query.filter_by(node_id=node_id) \
            .join(User, cls.author_id==User.uid) \
            .order_by(cls.created.desc()) \
            .add_columns(User.username, User.avator)
        return topics

    @classmethod
    def get_topic_by_id(cls,id=None):
        topic = cls.query.filter_by(id=id) \
            .join(Node, cls.node_id==Node.id) \
            .join(User, cls.author_id==User.uid) \
            .add_columns(Node.slug, Node.name, User.username, User.uid, User.avator)
        return topic

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

    @classmethod
    def get_replies_by_author(cls,author_id=None):
        replies = cls.query.filter_by(author_id=author_id) \
            .join(Topic, cls.topic_id==Topic.id) \
            .join(User, Topic.author_id==User.uid) \
            .order_by(cls.created.desc()) \
            .add_columns(User.username, Topic.title, Topic.id)
        return replies

    @classmethod
    def get_replies_by_topic_id(cls,topic_id=None):
        replies = Reply.query.filter_by(topic_id=topic_id) \
            .join(User, cls.author_id==User.uid) \
            .order_by(cls.created.desc()) \
            .add_columns(User.username, User.avator, User.uid)
        return replies

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key = True)
    owner_user_id = db.Column(db.Integer, nullable = True)
    involved_type = db.Column(db.Integer, nullable = True)
    involved_topic_id = db.Column(db.Integer, nullable = True)
    involved_reply_id = db.Column(db.Integer, nullable = True)
    created = db.Column(db.DateTime)

    @classmethod
    def get_fav_topics_by_user_uid(cls, uid=None):
        topics = cls.query.filter_by(involved_reply_id=uid) \
            .join(Topic, cls.involved_topic_id==Topic.id) \
            .join(Node, Topic.node_id==Node.id) \
            .join(User, Topic.author_id==User.uid) \
            .order_by(Topic.created.desc()) \
            .add_columns(User.username, User.uid, User.avator, Node.slug,Node.name,
                         Topic.id, Topic.title, Topic.last_replied_by,
                         Topic.last_replied_time, Topic.last_touched,
                         Topic.created, Topic.reply_count)
        return topics
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
