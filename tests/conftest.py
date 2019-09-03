import os
from urllib.parse import urlparse

import pytest
import factory

from demo_app import factories, models

from tests.utils import init_postgresql_database, drop_postgresql_database


class AppConfigTest(factories.AppConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'postgres://flask:flask@localhost/flask_test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture(scope='session')
def app(request):
    app_ = factories.create_app(AppConfigTest)

    db_uri = urlparse(app_.config['SQLALCHEMY_DATABASE_URI'])
    pg_host = db_uri.hostname
    pg_port = db_uri.port
    pg_user = db_uri.username
    pg_password = db_uri.password
    pg_db = db_uri.path[1:]

    init_postgresql_database(pg_user, pg_password, pg_host, pg_port, pg_db)

    factories.configure_db(app_)

    models.db.create_all()

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_password, pg_host, pg_port, pg_db)

    return app_


@pytest.fixture(scope='session')
def _db(app):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """
    return models.db


@pytest.fixture(scope='function')
def base_factory(db_session):
    class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
        """Base model factory."""

        class Meta:
            abstract = True
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = 'flush'

    return BaseFactory


@pytest.fixture(scope='function')
def category_factory(base_factory):
    class CategoryFactory(base_factory):
        class Meta:
            model = models.Category

        name = factory.Sequence(lambda n: u'Category %d' % n)

    return CategoryFactory


@pytest.fixture(scope='function')
def post_factory(base_factory, category_factory):

    class PostFactory(base_factory):
        class Meta:
            model = models.Post

        title = factory.Sequence(lambda n: u'Post Title %d' % n)
        body = factory.Sequence(lambda n: u'Post Body %d' % n)
        category = factory.SubFactory(category_factory)

    return PostFactory
