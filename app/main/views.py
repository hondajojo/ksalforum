#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, abort, jsonify, g
from . import main
from .forms import LoginForm, RegisterForm, CreateForm, ReplyForm
from ..models import User, Topic, Node, Plane, Reply, Favorite
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import login_required, login_user, logout_user, current_user
import datetime
from functools import wraps

@main.route('/')
def index():
    # topics = Topic.query.join(Node, Topic.node_id==Node.id).join(User, Topic.author_id==User.uid)
    query = db.session.query(Topic, Node, User)
    topics = query.join(Node, Topic.node_id==Node.id).join(User, Topic.author_id==User.uid).order_by(Topic.created.desc()).all()
    nodes = Node.query.all()
    user_count = User.query.count()
    node_count = Node.query.count()
    topic_count = Topic.query.count()
    reply_count = Reply.query.count()

    ''' how ugly code ! about plane and node'''
    f = Plane.query.all()
    planes = []
    for i in f:
        test = {}
        test['planename'] = i.name
        node = Node.query.filter_by(plane_id=i.id).all()
        test02 = []
        for x in node:
            test01 = {}
            test01['slug'] = x.slug
            test01['name'] = x.name
            test02.append(test01)
        test['plane_node'] = test02
        planes.append(test)

    if current_user.is_authenticated:
        user_topic_count = Topic.query.filter_by(author_id=current_user.uid).count()
        user_reply_count = Reply.query.filter_by(author_id=current_user.uid).count()
        user_favorite_count = Favorite.query.filter_by(involved_reply_id=current_user.uid).count()
    else:
        user_topic_count = None
        user_favorite_count = None
        user_reply_count = None

    return render_template('topic/topics.html', topics=topics, planes=planes, \
        nodes=nodes, user_count=user_count, node_count=node_count, \
        topic_count=topic_count, reply_count=reply_count, user_topic_count=user_topic_count, \
        user_reply_count=user_reply_count, user_favorite_count=user_favorite_count)

@main.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash(u'邮箱或密码错误!')
        else:
            flash_errors(form)
        return render_template('user/login.html',form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), created=datetime.datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('user/register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/setting', methods=['GET','POST'])
@login_required
def setting():
    user_info = User.query.filter_by(email=current_user.email).first()
    if request.method == 'POST':
        user_info.website = request.form['website']
        user_info.nickname = request.form['nickname']
        user_info.signature = request.form['signature']
        user_info.location = request.form['location']
        user_info.company = request.form['company']
        user_info.twitter = request.form['twitter']
        user_info.github = request.form['github']
        user_info.douban = request.form['douban']
        user_info.self_intro = request.form['self_intro']
        user_info.updated = datetime.datetime.utcnow()
        db.session.add(user_info)
        db.session.commit()
        flash(u'保存成功')
        return redirect(url_for('main.setting'))
    return render_template('user/setting.html', user_info=user_info)

@main.route('/t/create/<node>', methods=['GET','POST'])
@login_required
def create(node):
    nodes = Node.query.filter_by(slug=node).first_or_404()
    user_info = User.query.filter_by(email=current_user.email).first()
    current_user_topics_count = Topic.query.filter_by(author_id=current_user.uid).count()
    form = CreateForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        created = datetime.datetime.utcnow()
        author_id = current_user.uid
        node_id = nodes.id
        topic = Topic(title=title, content=content, created=created, author_id=author_id, node_id=node_id)
        nodes.topic_count += 1
        db.session.add(topic)
        db.session.add(nodes)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('topic/create.html', form=form, user_info=user_info, node=node, current_user_topics_count=current_user_topics_count)

def hit(f):
    @wraps(f)
    def wrapper(id):
        topic = Topic.query.filter_by(id=id).first_or_404()
        topic.hits += 1
        db.session.add(topic)
        db.session.commit()
        return f(id)
    return wrapper

@main.route('/t/<int:id>', methods=['GET','POST'])
@hit
def view(id):
    query = db.session.query(Topic, Node, User)
    topic = query.filter_by(id=id).join(Node, Topic.node_id==Node.id).join(User, Topic.author_id==User.uid).first()
    replies = db.session.query(Reply, User).filter_by(topic_id=id).join(User, Reply.author_id==User.uid).order_by(Reply.created.desc()).all()
    topic_favorited = None
    if current_user.is_authenticated:
        topic_favorited = Favorite.query.filter_by(involved_reply_id=current_user.uid).filter_by(involved_topic_id=id).first()

    if current_user.is_authenticated:
        user_topic_count = Topic.query.filter_by(author_id=current_user.uid).count()
        user_reply_count = Reply.query.filter_by(author_id=current_user.uid).count()
        user_favorite_count = Favorite.query.filter_by(involved_reply_id=current_user.uid).count()
    else:
        user_topic_count = None
        user_favorite_count = None
        user_reply_count = None

    form = ReplyForm()
    if topic:
        if form.validate_on_submit():
            content = form.content.data
            topic_id = id
            author_id = current_user.uid
            created = datetime.datetime.utcnow()
            reply = Reply(content=content, topic_id=topic_id, author_id=author_id, created=created)

            topic = Topic.query.filter_by(id=id).first_or_404()
            if not topic.reply_count:
                topic.reply_count = 0
            topic.reply_count += 1
            topic.last_replied_by = current_user.username
            topic.last_replied_time = created
            topic.last_touched = created

            db.session.add(reply)
            db.session.add(topic)
            db.session.commit()
            return redirect('/t/%s' % id)
        else:
            flash_errors(form)
        return render_template('topic/view.html', topic=topic, form=form, \
            replies=replies, topic_favorited=topic_favorited, user_reply_count=user_reply_count, \
            user_topic_count=user_topic_count, user_favorite_count=user_favorite_count)
    else:
        abort(404)

@main.route('/favorite', methods=['GET', 'POST'])
def favorite():
    owner_user_id = request.args.get('owner_user_id',0)
    involved_type = request.args.get('involved_type',0)
    involved_topic_id = request.args.get('involved_topic_id',0)
    created = datetime.datetime.utcnow()

    have_topic = Topic.query.filter_by(id=involved_topic_id).first()

    if current_user.is_authenticated:
        have_fav = Favorite.query.filter_by(involved_topic_id=involved_topic_id).filter_by(involved_reply_id=current_user.uid).first()

        if not have_topic:
            return jsonify({'success':0,'message':'topic_not_exist'})
        if int(owner_user_id) == int(current_user.uid):
            return jsonify({'success':0,'message':'can_not_favorite_your_topic'})
        if have_fav:
            return jsonify({'success':0,'message':'already_favorited'})

        favorite = Favorite(owner_user_id=owner_user_id,involved_type=involved_type,involved_topic_id=involved_topic_id,involved_reply_id=current_user.uid,created=created)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'success':1,'message':'favorite_success'})
    else:
        return jsonify({'success':0,'message':'user_not_login'})


@main.route('/unfavorite', methods=['GET' ,'POST'])
def unfavorite():
    owner_user_id = request.args.get('owner_user_id',0)
    involved_topic_id = request.args.get('involved_topic_id',0)
    have_topic = Topic.query.filter_by(id=involved_topic_id).first()
    if current_user.is_authenticated:
        have_fav = Favorite.query.filter_by(involved_topic_id=involved_topic_id).filter_by(involved_reply_id=current_user.uid).first()
        if not have_topic:
            return jsonify({'success':0,'message':'topic_not_exist'})
        if not have_fav:
            return jsonify({'success':0,'message':'not_been_favorited'})
        Favorite.query.filter_by(involved_topic_id=involved_topic_id).filter_by(involved_reply_id=current_user.uid).delete()
        return jsonify({'success':1,'message':'favorite_success'})
    return jsonify({'success':0,'message':'user_not_login'})

@main.route('/node/<node_slug>')
def node(node_slug):
    node = Node.query.filter_by(slug=node_slug).first_or_404()
    query = db.session.query(Topic, User)
    topics = query.filter_by(node_id=node.id).join(User, Topic.author_id==User.uid).order_by(Topic.created.desc()).all()
    if current_user.is_authenticated:
        user_topic_count = Topic.query.filter_by(author_id=current_user.uid).count()
        user_reply_count = Reply.query.filter_by(author_id=current_user.uid).count()
        user_favorite_count = Favorite.query.filter_by(involved_reply_id=current_user.uid).count()
    else:
        user_topic_count = None
        user_favorite_count = None
        user_reply_count = None
    # topics = Topic.query.filter_by(node_id=node.id).order_by(created.desc()).all()
    return render_template('topic/node_topics.html', node=node, topics=topics, \
        user_topic_count=user_topic_count, user_reply_count=user_reply_count, \
        user_favorite_count=user_favorite_count)

@main.route('/t/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_topic(id):
    topic = Topic.query.filter_by(id=id).first_or_404()

    user_topic_count = Topic.query.filter_by(author_id=current_user.uid).count()
    user_reply_count = Reply.query.filter_by(author_id=current_user.uid).count()
    user_favorite_count = Favorite.query.filter_by(involved_reply_id=current_user.uid).count()

    form = CreateForm()
    if form.validate_on_submit():
        topic.title = form.title.data
        topic.content = form.content.data
        topic.updated = datetime.datetime.utcnow()
        db.session.add(topic)
        db.session.commit()
        return redirect('/t/%s' %id)
    else:
        flash_errors(form)
    form.content.data = topic.content
    form.title.data = topic.title
    return render_template('topic/edit.html', user_topic_count=user_topic_count, \
        user_favorite_count=user_favorite_count, user_reply_count=user_reply_count, form=form)


@main.route('/reply/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reply(id):
    reply = Reply.query.filter_by(id=id).first_or_404()
    form = ReplyForm()
    user_topic_count = Topic.query.filter_by(author_id=current_user.uid).count()
    user_reply_count = Reply.query.filter_by(author_id=current_user.uid).count()
    user_favorite_count = Favorite.query.filter_by(involved_reply_id=current_user.uid).count()

    if form.validate_on_submit():
        reply.content = form.content.data
        reply.updated = datetime.datetime.utcnow()
        db.session.add(reply)
        db.session.commit()
        return redirect('/t/%s' % reply.topic_id)
    else:
        flash_errors(form)
    form.content.data = reply.content
    return render_template('topic/reply_edit.html', form=form, user_topic_count=user_topic_count, \
        user_favorite_count=user_favorite_count, user_reply_count=user_reply_count)

"""
an ajax example
"""
@main.route('/echo', methods=['GET', 'POST'])
def ajax():
    ret_data = {'233':'hehe'}
    # ret_data = {'value':request.get.args['echoValue']}
    # return jsonify(ret_data)
    return render_template('topic/ajax.html')

@main.route('/echo2', methods=['GET','POST'])
def ajax2():
    print '233'
    ff = request.args.get('x')
    print ff
    return jsonify({'hehe':ff})
@main.route('/ajax')
def ajax3():
    ids = request.args.get('id')
    print ids
    data = {'papa':ids}
    # return request.args.get('id')
    return jsonify(data)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'%s - %s' % (getattr(form, field).label.text, error), 'error')

@main.route('/secret')
@login_required
def secret():
    return 'you have login in'
