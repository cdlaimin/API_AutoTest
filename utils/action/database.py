import pymysql

from conf import settings
from utils.libs.exception import DbConfigNotExist
from utils.tools.singleton import Singleton


class Database(metaclass=Singleton):
    """数据库相关操作封装"""
    def __init__(self, app):
        """初始化数据库连接对象"""
        db_config = settings.DB_CONFIG.get(app)
        if db_config is None:
            raise DbConfigNotExist
        try:
            db_config['port'] = int(db_config['port'])
            # 创建链接
            self.conn = pymysql.Connect(**db_config)
        except Exception:
            raise
        else:
            self.cursor = self.conn.cursor()

    def query_one(self, sql):
        """
        查询单条数据
        :param sql:
        :return: (字段1，字段2，..)
        """
        try:
            self.cursor.execute(sql)
        except Exception:
            raise
        else:
            return self.cursor.fetchone()

    def query_many(self, sql):
        """
        查询多条条数据
        :param sql:
        :return: ((字段1，字段2，..),(字段1，字段2，..),(字段1，字段2，..))
        """
        try:
            self.cursor.execute(sql)
        except Exception:
            raise
        else:
            return self.cursor.fetchall()

    def execute_one(self, sql):
        """
        执行数据库单次操作
        :param sql:
        :return: none
        """
        try:
            self.cursor.execute(sql)
        except Exception:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def execute_many(self, sql, params: list):
        """
        执行数据库批量操作。
        :param sql: sql中需要有占位符接收param
        :return: none
        """
        try:
            self.cursor.executemany(sql, params)
        except Exception:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def close(self):
        """
        关闭链接
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    app_name = 'meiduo'
    sql = 'select * from tb_sku'
    db = Database(app_name).query_many(sql)
    print(db)
