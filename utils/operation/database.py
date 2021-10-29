import pymysql
from loguru import logger
from pymysql.cursors import DictCursor

from conf import DB_CONF, ACCOUNT
from utils.suport.exception import ConfNotExist
from utils.suport.singleton import Singleton


class DataBase(metaclass=Singleton):
    """数据库相关操作封装"""

    def __init__(self, target):
        """初始化数据库连接对象"""
        self.account = ACCOUNT.get(target)

        db_config = DB_CONF.get(target)
        if db_config is None:
            raise ConfNotExist('数据库配置信息不存在')
        try:
            db_config['port'] = int(db_config['port'])
            db_config['cursorclass'] = DictCursor
            # 创建链接
            self.conn = pymysql.Connect(**db_config)
        except Exception:
            raise
        else:
            self.cursor = self.conn.cursor()
            logger.info(f'目标数据库 {target} 链接成功。')

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def query_one(self, sql):
        """
        查询单条数据
        :param sql:
        :return: (字段1，字段2，..)
        """
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            logger.info(f"{sql}  >> 执行失败 ！！ \n {e}")
            result = None

        return result

    def query_many(self, sql, param=None, size=None):
        """
        执行查询，并取出多条结果集
        @param sql:查询sql，多条件使用参数[param]传递进来。sql中的字符型占位符，需要加""，例如 where name = "%s"
        @param param: 可选参数，条件列表值（元组/列表）
        @param size: 查询条数
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, param)
            if size:
                result = self.cursor.fetchmany(size)
            else:
                result = self.cursor.fetchall()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            logger.info(f"{sql}  >> 执行失败 ！！ \n {e}")
            result = None

        return result

    def execute_one(self, sql):
        """
        执行数据库单次操作
        :param sql:
        :return: none
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            self.conn.rollback()
            logger.info(f"{sql}  >> 执行失败 ！！ \n {e}")

    def execute_many(self, sql, param):
        """
        增删改操作多条数据
        @param sql:要插入的sql，需要占位符占位
        @param param:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        try:
            self.cursor.executemany(sql, param)
            self.conn.commit()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            self.conn.rollback()
            logger.info(f"{sql}  >> 执行失败 ！！ \n {e}")
