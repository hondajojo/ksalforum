#!/usr/bin/env python

from functools import wraps
from .models import Topic
from . import db

def hit(f):
    @wraps(f)
    def wrapper(id):
        topic = Topic.query.filter_by(id=id).first_or_404()
        topic.hits += 1
        db.session.add(topic)
        db.session.commit()
        return f(id)
    return wrapper
