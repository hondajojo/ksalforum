from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from flask.ext.moment import Moment

login_manager = LoginManager()
mail = Mail()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'
bootstrap = Bootstrap()
babel = Babel()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    # app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    return app
