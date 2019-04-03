from flask import Flask


from . import controllers


class AppConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flask:flask@localhost/flask'


def configure_db(app):
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    app.register_blueprint(controllers.blog)
    return app
