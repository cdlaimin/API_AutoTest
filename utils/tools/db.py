import pymysql
from pymysql.cursors import DictCursor

from conf import DATABASE
from utils.suport import logger
from utils.suport import Singleton
from utils.suport.exception import ConfNotExist


class DataBase(metaclass=Singleton):
    """数据库相关操作封装"""

    def __init__(self, env):
        """初始化数据库连接对象"""

        config = DATABASE.get(env + '_mysql')
        if config is None:
            raise ConfNotExist
        try:
            config['port'] = int(config['port'])
            config['cursorclass'] = DictCursor
            # 创建链接
            self.conn = pymysql.Connect(**config)
        except Exception:
            raise
        else:
            self.cursor = self.conn.cursor()
            logger.info(f'目标数据库 {env} 链接成功。')

    def __del__(self):
        if hasattr(self, "cursor"):
            self.cursor.close()
        if hasattr(self, "conn"):
            self.conn.close()

    def query_one(self, sql, params=None):
        """
        查询单条数据
        :param sql:
        :param params: 可选参数。替换sql中的占位符，格式:[value1, value2, ...]
        :return: (字段1，字段2，..)
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            result = self.cursor.fetchone()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            logger.info(f"{sql}  -- 执行失败 !!\n {e}")
            result = None

        return result

    def query_many(self, sql, params=None, size=None):
        """
        执行查询，并取出多条结果集
        @param sql:查询sql，多条件使用参数[param]传递进来。sql中的字符型占位符，需要加""，例如 where name = "%s"
        @param params: 可选参数，条件列表值（元组/列表）。格式: [value1,value2,...]
        @param size: 查询条数
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        try:
            if params is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, params)
            if size:
                result = self.cursor.fetchmany(size)
            else:
                result = self.cursor.fetchall()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            logger.info(f"{sql}  -- 执行失败 !!\n {e}")
            result = None

        return result

    def execute_one(self, sql, param=None):
        """
        执行数据库单次操作
        :param sql:
        :param param: 可选参数。替换sql中的占位符，格式:[value1, value2, ...]
        :return: none
        """
        try:
            if param:
                self.cursor.execute(sql, param)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            logger.info(f"{sql}  -- 执行成功 !!")

        except Exception as e:
            self.conn.rollback()
            logger.info(f"{sql}  -- 执行失败 !!\n {e}")

    def execute_many(self, sql, params):
        """
        增删改操作多条数据
        @param sql:要插入的sql，需要占位符占位
        @param params:要插入的记录的多组数据，格式:[[],[],...]
        @return: count 受影响的行数
        """
        try:
            self.cursor.executemany(sql, params)
            self.conn.commit()
            logger.info(f"{sql}  -- 执行成功 !!")
        except Exception as e:
            self.conn.rollback()
            logger.info(f"{sql}  -- 执行失败 !!\n {e}")
