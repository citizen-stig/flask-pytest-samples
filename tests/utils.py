# Whole module copied from pytest-postgresql, but I needed password support.
import time
import socket

import psycopg2


def wait_for_port(host, port, sleep_time=0.5, timeout=5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        sleep_time (float): How much time to wait between attempts
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(sleep_time)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the port {} on host {} to start accepting '
                                   'connections.'.format(port, host)) from ex


def init_postgresql_database(user, password, host, port, db):
    wait_for_port(host, port=5432)
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
