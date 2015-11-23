import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN =True
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
    FLASKY_POSTS_PER_PAGE = 10
    # PERMANENT_SESSION_LIFETIME = 15

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cm1130335361@163.com'
    MAIL_PASSWORD = '6776383071'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'cm1130335361@163.com'

    @staticmethod
    def init_app(app):
        pass

class Developmentconfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:1@127.0.0.1/f22e'

config = {
    'default':Developmentconfig,
}
