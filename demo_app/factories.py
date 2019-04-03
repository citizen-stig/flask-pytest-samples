import warnings

from flask import Flask


from . import controllers
from . import models


class AppConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flask:flask@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def configure_db(app):
    db = models.db
    db.app = app
    db.init_app(app)
    # Only for simplicity
    db.create_all()
    return db


def create_app():
    filter_warnings()
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    app.register_blueprint(controllers.blog)
    configure_db(app)
    return app


def filter_warnings():
    warnings.filterwarnings(
        'ignore',
        message='The psycopg2 wheel package will be renamed from release 2.8')
