import warnings

from flask import Flask

from .models import db
from . import controllers


class AppConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flask:flask@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config=None):
    filter_warnings()
    app = Flask(__name__)
    if config is None:
        config = AppConfig
    app.config.from_object(config)
    app.register_blueprint(controllers.blog)
    return app


def configure_db(app):
    db.app = app
    db.init_app(app)
    return db


def filter_warnings():
    warnings.filterwarnings(
        'ignore',
        message='The psycopg2 wheel package will be renamed from release 2.8')
