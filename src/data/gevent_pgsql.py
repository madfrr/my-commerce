from __future__ import print_function

# pylint:disable=import-error,broad-except,bare-except
from utils.logger import logger
from gevent.queue import Queue
from gevent.socket import wait_read, wait_write
from psycopg2 import extensions, OperationalError, connect
from psycopg2.extras import execute_values
import sys
import contextlib
import gevent
import time

if sys.version_info[0] >= 3:
    integer_types = (int,)
else:
    import __builtin__

    integer_types = (int, __builtin__.long)

tag = '[Connection_Pool] |'


def gevent_wait_callback(conn, timeout=None):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise OperationalError("Bad result from poll: %r" % state)


extensions.set_wait_callback(gevent_wait_callback)


class AbstractDatabaseConnectionPool(object):
    def __init__(self, maxsize=10):
        if not isinstance(maxsize, integer_types):
            raise TypeError("Expected integer, got %r" % (maxsize,))
        self.maxsize = maxsize
        self.pool = Queue(maxsize=maxsize)
        self.size = 0

    def create_connection(self):
        raise NotImplementedError()

    def get(self):
        pool = self.pool

        logger.info(
            f"{tag}  open_connections_count: {self.size} / pool_size: {pool.qsize()}  max_connections:{self.maxsize}")

        try:
            if self.size >= self.maxsize or pool.qsize():
                conn = pool.get(block=False, timeout=2)
                logger.info(f"{tag}  got connection from pool")
                return conn
        except:
            pass

        logger.info(f"{tag}  could not get a connection from pool")

        self.size += 1
        try:
            new_item = self.create_connection()
            logger.info(f"{tag}  new connection created")
        except Exception as e:
            logger.error(e)
            self.size -= 1
            raise
        return new_item

    def put(self, item):
        logger.info(f"{tag} putting connection back to pool")
        self.pool.put(item)

    def closeall(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            try:
                conn.close()
            except Exception:
                pass

    @contextlib.contextmanager
    def connection(self, isolation_level=None):
        conn = self.get()
        try:
            if isolation_level is not None:
                if conn.isolation_level == isolation_level:
                    isolation_level = None
                else:
                    conn.set_isolation_level(isolation_level)
            yield conn
        except:
            if conn.closed:
                conn = None
                self.closeall()
            else:
                conn = self._rollback(conn)
            raise
        else:
            if conn.closed:
                raise OperationalError(
                    "Cannot commit because connection was closed: %r" % (conn,)
                )
            conn.commit()
        finally:
            if conn is not None and not conn.closed:
                if isolation_level is not None:
                    conn.set_isolation_level(isolation_level)
                self.put(conn)

    @contextlib.contextmanager
    def cursor(self, *args, **kwargs):
        isolation_level = kwargs.pop("isolation_level", None)
        with self.connection(isolation_level) as conn:
            yield conn.cursor(*args, **kwargs)

    def _rollback(self, conn):
        try:
            conn.rollback()
        except:
            gevent.get_hub().handle_error(conn, *sys.exc_info())
            return
        return conn

    def execute(self, *args, **kwargs):
        with self.cursor(**kwargs) as cursor:
            cursor.execute(*args)
            return cursor

    def execute_values(self, insert_query, data, **kwargs):
        with self.cursor() as cursor:
            return execute_values(cursor, insert_query, data, **kwargs)

    def execute_many(self, insert_query, data, **kwargs):
        with self.cursor() as cursor:
            return cursor.executemany(insert_query, data, **kwargs)

    def fetchone(self, *args, **kwargs):
        with self.cursor(**kwargs) as cursor:
            cursor.execute(*args)
            return cursor.fetchone()

    def fetchall(self, *args, **kwargs):
        with self.cursor(**kwargs) as cursor:
            cursor.execute(*args)
            return cursor.fetchall()

    def fetchall_cursor(self, *args, **kwargs):
        with self.cursor(**kwargs) as cursor:
            cursor.execute(*args)
            return cursor

    def fetchiter(self, *args, **kwargs):
        with self.cursor(**kwargs) as cursor:
            cursor.execute(*args)
            while True:
                items = cursor.fetchmany()
                if not items:
                    break
                for item in items:
                    yield item


class PostgresConnectionPool(AbstractDatabaseConnectionPool):
    def __init__(self, dbname, user, password, host, port, *args, **kwargs):
        self.connect = kwargs.pop("connect", connect)
        maxsize = kwargs.pop("maxsize", None)
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.args = args
        self.kwargs = kwargs
        AbstractDatabaseConnectionPool.__init__(self, maxsize)

    def create_connection(self):
        logger.debug(f'Iniciando conexao com o {self.dbname}')
        s = time.time()

        connection = self.connect(dbname=self.dbname,
                                  user=self.user,
                                  password=self.password,
                                  host=self.host,
                                  port=self.port,
                                  keepalives=1,
                                  keepalives_idle=5,
                                  keepalives_interval=2,
                                  keepalives_count=2,
                                  **self.kwargs)

        logger.debug(
            f'Conectado com sucesso ao {self.dbname} ->  {time.time() - s} segundos')
        connection.set_session(autocommit=False)

        return connection
