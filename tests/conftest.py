from urllib.parse import urlparse

import pytest


from demo_app import factories

from tests.utils import init_postgresql_database, drop_postgresql_database


class AppConfigTest(factories.AppConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flask:flask@localhost/flask_test'


@pytest.fixture(scope='session')
def app(request):
    db_uri = urlparse(AppConfigTest.SQLALCHEMY_DATABASE_URI)
    pg_host = db_uri.hostname
    pg_port = db_uri.port
    pg_user = db_uri.username
    pg_password = db_uri.password
    pg_db = db_uri.path[1:]

    init_postgresql_database(pg_user, pg_password, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_password, pg_host, pg_port, pg_db)

    return factories.create_app(AppConfigTest)
