# 数据库操作
import pymysql
from config import DB_CONFIG

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)

def query_one(sql, params=None):
    """执行查询，返回单条记录"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    finally:
        conn.close()

def query_all(sql, params=None):
    """执行查询，返回所有记录"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute_sql(sql, params=None):
    """执行增删改，返回影响行数"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, params)
            conn.commit()
            return rows
    finally:
        conn.close()

def delete_test_user(username):
    """删除测试用户（物理删除）"""
    sql = "DELETE FROM `user` WHERE username = %s"
    return execute_sql(sql, (username,))