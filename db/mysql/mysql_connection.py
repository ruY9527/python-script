# -*- coding: utf-8 -*-
"""
MySQL 数据库连接工具类
提供可复用的数据库连接、查询、执行等功能
"""

import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple


class MySQLConnection:
    """MySQL 数据库连接类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化数据库连接配置
        
        Args:
            config: 数据库连接配置字典，包含以下键:
                - host: 数据库地址
                - port: 端口 (默认 3306)
                - user: 用户名
                - password: 密码
                - database: 数据库名
                - charset: 字符集 (默认 utf8mb4)
        """
        self.config = {
            'host': config.get('host', 'localhost'),
            'port': config.get('port', 3306),
            'user': config.get('user', 'root'),
            'password': config.get('password', ''),
            'database': config.get('database'),
            'charset': config.get('charset', 'utf8mb4'),
            'cursorclass': config.get('cursorclass', DictCursor)
        }
        self.connection: Optional[pymysql.Connection] = None
    
    def connect(self) -> pymysql.Connection:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**self.config)
            print(f"成功连接到数据库 {self.config['database']}")
            return self.connection
        except pymysql.Error as e:
            print(f"连接数据库失败：{e}")
            raise
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("数据库连接已关闭")
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.connection is not None and self.connection.open
    
    @contextmanager
    def cursor(self, cursor_class=None):
        """
        上下文管理器获取游标
        
        Usage:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM table")
        """
        if not self.is_connected():
            self.connect()
        
        cursor = self.connection.cursor(cursor_class or self.config['cursorclass'])
        try:
            yield cursor
        finally:
            cursor.close()
    
    def execute(self, sql: str, params: Optional[Tuple] = None) -> int:
        """
        执行 SQL 语句 (INSERT, UPDATE, DELETE)
        
        Args:
            sql: SQL 语句
            params: 参数元组
            
        Returns:
            受影响的行数
        """
        with self.cursor() as cursor:
            cursor.execute(sql, params or ())
            self.connection.commit()
            return cursor.rowcount
    
    def query(self, sql: str, params: Optional[Tuple] = None) -> List[Dict]:
        """
        查询 SQL 语句 (SELECT)
        
        Args:
            sql: SQL 语句
            params: 参数元组
            
        Returns:
            查询结果列表
        """
        with self.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    
    def query_one(self, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        """
        查询单条记录
        
        Args:
            sql: SQL 语句
            params: 参数元组
            
        Returns:
            单条记录或 None
        """
        with self.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()
    
    def get_tables(self) -> List[str]:
        """获取所有表名"""
        with self.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            result = cursor.fetchall()
            return [list(table.values())[0] for table in result]
    
    def get_table_columns(self, table_name: str) -> List[Dict]:
        """
        获取表的列信息
        
        Args:
            table_name: 表名
            
        Returns:
            列信息列表
        """
        with self.cursor() as cursor:
            cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
            return cursor.fetchall()
    
    def batch_execute(self, sql: str, params_list: List[Tuple]) -> int:
        """
        批量执行 SQL 语句
        
        Args:
            sql: SQL 语句
            params_list: 参数列表
            
        Returns:
            受影响的行数
        """
        with self.cursor() as cursor:
            cursor.executemany(sql, params_list)
            self.connection.commit()
            return cursor.rowcount


# 示例配置
DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'your_database',
    'charset': 'utf8mb4'
}


if __name__ == "__main__":
    # 使用示例
    db = MySQLConnection(DEFAULT_CONFIG)
    
    try:
        # 连接数据库
        db.connect()
        
        # 查询示例
        results = db.query("SELECT * FROM your_table LIMIT 10")
        print(f"查询结果：{results}")
        
        # 获取所有表
        tables = db.get_tables()
        print(f"表列表：{tables}")
        
        # 执行插入
        # affected = db.execute(
        #     "INSERT INTO your_table (name, value) VALUES (%s, %s)",
        #     ("test", 123)
        # )
        # print(f"受影响行数：{affected}")
        
    except Exception as e:
        print(f"错误：{e}")
    finally:
        db.disconnect()
