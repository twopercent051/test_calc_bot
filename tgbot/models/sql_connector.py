import asyncio

import pymysql
from create_bot import config
import time


def connection_init():
    host = config.db.host
    user = config.db.user
    password = config.db.password
    db_name = config.db.database
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def sql_start():
    connection = connection_init()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                          CREATE TABLE IF NOT EXISTS users(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                          user_id VARCHAR(40),
                          username VARCHAR(40));
                          """)
            cursor.execute("""
                          CREATE TABLE IF NOT EXISTS operations(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                          user_id VARCHAR(40),
                          timestamp INT,
                          operation VARCHAR(40),
                          result FLOAT(5));
                          """)
        print('MySQL started')
    finally:
        connection.close()


async def check_user_sql(user_id):
    connection = connection_init()
    query = 'SELECT COUNT(user_id) AS num_users FROM users WHERE user_id = (%s);'
    query_tuple = (user_id,)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
            result = cursor.fetchone()
        if result['num_users'] > 0:
            return True
        else:
            return False
    finally:
        connection.commit()
        connection.close()


async def create_user_sql(user_id, username):
    connection = connection_init()
    query = 'INSERT INTO users (user_id, username) VALUES (%s, %s);'
    query_tuple = (user_id, username)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def create_operation_sql(user_id, operation, result):
    connection = connection_init()
    timestamp = time.time()
    query = 'INSERT INTO operations (user_id, timestamp, operation, result) VALUES (%s, %s, %s, %s);'
    query_tuple = (user_id, timestamp, operation, result)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_static_sql(user_id):
    connection = connection_init()
    query = 'SELECT operation, result FROM operations WHERE user_id = (%s);'
    query_tuple = (user_id,)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
            result = cursor.fetchall()
            print(result)
            return result
    finally:
        connection.commit()
        connection.close()


