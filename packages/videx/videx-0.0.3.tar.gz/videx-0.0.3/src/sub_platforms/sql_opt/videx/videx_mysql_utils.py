"""
Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
SPDX-License-Identifier: MIT

@ author: kangrong
@ date: 2025-03-13

 DB connection pool DBUtils https://webwareforpython.github.io/DBUtils/main.html
"""
import logging
import traceback
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pandas as pd
from dataclasses_json import dataclass_json
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB
from sqlalchemy import create_engine


class DBTYPE(Enum):
    OPEN_MYSQL = "OPEN_MYSQL"
    SQLITE = "SQLITE"


@dataclass_json
@dataclass
class MySQLConnectionConfig:
    dbtype: DBTYPE
    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 3306
    schema: Optional[str] = None
    user: Optional[str] = None
    pwd: Optional[str] = None
    consul: Optional[str] = None
    charset: Optional[str] = "utf8"
    initial_pool_size: Optional[int] = 5
    max_pool_size: Optional[int] = 10
    read_timeout: Optional[int] = 30
    write_timeout: Optional[int] = 30
    connect_timeout: Optional[int] = 10


def get_mysql_utils(config: MySQLConnectionConfig):
    if config.dbtype == DBTYPE.OPEN_MYSQL:
        return OpenMySQLUtils(config)
    else:
        raise Exception('not support datasource')


class AbstractMySQLUtils(object):

    def __init__(self, mysql_type, database, charset, read_timeout=30, write_timeout=30, connect_timeout=10):
        self.mysql_type = mysql_type
        self.database = database
        self.charset = charset
        self.pool = None
        self.pool_type = None
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.connect_timeout = connect_timeout
        pass

    def get_connection(self):
        pass

    def switch_db(self, db_name):
        if db_name == self.database:
            return
        self.database = db_name
        self.reconstruct_pool()

    def reconstruct_pool(self):
        if self.pool is not None:
            self.pool.close()
            if self.pool_type == 'PooledDB':
                self.get_shared_pool()
            else:
                self.get_persistent_pool()

    def get_shared_pool(self, initial_connections=1, max_connections=10):
        """
        Get a shared connection pool, suitable for applications that frequently create and destroy threads
        (for multi-process scenarios, each process should create its own connection pool).
        Args:
            initial_connections: Initial number of connections
            max_connections: Maximum number of connections, exceeding this number will result in an error,
                            passing 0 or not passing any value means no limit

        Returns:

        """
        self.pool = PooledDB(self.get_connection, mincached=initial_connections, maxconnections=max_connections)
        self.pool_type = 'PooledDB'
        return self.pool

    def get_persistent_pool(self):
        """
        Get a thread-bound connection pool where a connection is used by a single thread until the thread exits.
        Suitable for applications with a fixed number of threads.

        Returns:

        """
        self.pool = PersistentDB(self.get_connection)
        self.pool_type = 'PersistentDB'
        return self.pool

    def query_for_dataframe(self, sql_template: str, params: list = None) -> pd.DataFrame:
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection(True) as connection:
            return query_for_dataframe(connection, sql_template, params)

    def query_for_value(self, sql_template: str, params: list = None):
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection(True) as connection:
            return query_for_value(connection, sql_template, params)

    def execute_query(self, sql: str, params: list = None):
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection() as c:
            with c.cursor() as cursor:
                cursor.execute(sql, params)
                c.commit()
                if cursor.rowcount > 0:
                    return cursor.fetchall()
                else:
                    return None

    def execute_manyquery(self, sql: str, params: list = None):
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection() as c:
            with c.cursor() as cursor:
                cursor.executemany(sql, params)
                c.commit()
                if cursor.rowcount > 0:
                    return cursor.fetchall()
                else:
                    return None

    def execute_insert_with_transaction(self, sql: str, params: list = None):
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection() as c:
            with c.cursor() as cursor:
                cursor.execute(sql, params)
                inserted_id = cursor.lastrowid
            c.commit()
            c.close()
        return inserted_id

    def batch_execute_with_transaction(self, sql_list: list) -> bool:
        success = True
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection() as c:
            with c.cursor() as cursor:
                try:
                    for sql in sql_list:
                        cursor.execute(sql)
                    c.commit()
                    success = True
                except Exception as e:
                    print(e)
                    c.rollback()
                    success = False
            c.close()
        return success

    def execute_with_rollback(self, sql: str, params):
        if self.pool is None:
            self.pool = self.get_shared_pool()
        with self.pool.connection() as c:
            with c.cursor() as cursor:
                cursor.execute(sql, params)
                c.rollback()

    def destory(self):
        if self.pool is not None:
            try:
                self.pool.close()
            except Exception as e:
                logging.warning(f"close connection pool failed, {e}, {traceback.format_exc()}")


class OpenMySQLUtils(AbstractMySQLUtils):
    """
    Open-source MySQL connection class, which is used to connect with host, port, user and password.
    """

    def __init__(self, config: MySQLConnectionConfig):
        super().__init__('open_mysql', config.schema, config.charset,
                         config.read_timeout, config.write_timeout, config.connect_timeout)
        self.host = config.host
        self.port = config.port
        self.user = config.user
        self.password = config.pwd

    def get_connection(self):
        import pymysql
        return pymysql.connect(user=self.user,
                               password=self.password,
                               db=self.database,
                               charset=self.charset if self.charset is not None else 'utf8',
                               host=self.host,
                               port=self.port,
                               read_timeout=self.read_timeout,
                               write_timeout=self.write_timeout,
                               connect_timeout=self.connect_timeout)


    def get_sqlalchemy_engine(self, dbname: str = None):
        dbname = dbname if dbname is not None else self.database
        return create_engine(
            "mysql+pymysql://{user}:{pw}@[{host}]:{port}/{db}".format(host=self.host, port=self.port, db=dbname,
                                                                      user=self.user,
                                                                      pw=urllib.parse.quote_plus(self.password)))

    def __repr__(self):
        return f"OpenMySQL:{self.host}:{self.port}/{self.database}"

    def __str__(self):
        return self.__repr__()


def _parse_col_names(cursor):
    col_names = []
    if cursor.rowcount == 0:
        return col_names
    for desc in cursor.description:
        col_names.append(desc[0])
    return col_names


def query_for_dataframe(connection, sql_template: str, params: list = None):
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_template, params)
                col_names = _parse_col_names(cursor)
                data = cursor.fetchall()
                connection.commit()
                data = list(map(list, data))
                return pd.DataFrame(data, columns=col_names)
            except Exception as e:
                logging.error(f"query_for_dataframe failed, sql: {cursor.mogrify(sql_template, params)}, error: {e}")
                raise e


def query_for_value(connection, sql_template: str, params: list = None):
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_template, params)
                data = cursor.fetchone()
                connection.commit()
                if data is None:
                    return None
                return data[0]
            except Exception as e:
                logging.error(f"query_for_value failed, sql: {cursor.mogrify(sql_template, params)}, error: {e}")
                raise e
