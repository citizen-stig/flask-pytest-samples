# Whole module copied from pytest-postgresql, but I needed password support.
import psycopg2


def init_postgresql_database(user, password, host, port, db):
    conn = psycopg2.connect(user=user, host=host, password=password, port=port, dbname='postgres')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('CREATE DATABASE {0};'.format(db))
    cur.close()
    conn.close()


def drop_postgresql_database(user, password, host, port, db):
    conn = psycopg2.connect(user=user, host=host, password=password, port=port)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    # We cannot drop the database while there are connections to it, so we
    # terminate all connections first while not allowing new connections.
    pid_column = 'pid'
    cur.execute(
        'UPDATE pg_database SET datallowconn=false WHERE datname = %s;',
        (db,))
    cur.execute(
        'SELECT pg_terminate_backend(pg_stat_activity.{0})'
        'FROM pg_stat_activity WHERE pg_stat_activity.datname = %s;'.format(
            pid_column),
        (db,))
    cur.execute('DROP DATABASE IF EXISTS {0};'.format(db))
    cur.close()
    conn.close()
