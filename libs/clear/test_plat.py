from conf import ACCOUNT
from utils.factory import ClearDB
from utils.suport.other import switch_name
from utils.tools.db import DataBase
from utils.suport.singleton import Singleton


class TestPlat(DataBase, metaclass=Singleton):
    """数据库相关操作"""

    def __init__(self, env):
        self.server = switch_name(self.__class__.__name__)
        super().__init__(self.server, env)

        # 获取当前服务的账号信息
        users = ACCOUNT[self.server]

        # 根据账号查表，获得用户ID信息
        self.ids = []
        sql = 'SELECT id FROM test_plat.tp_users WHERE username = %s;'
        for params in [value.get("username") for value in users.values()]:
            self.ids.append(self.query_one(sql=sql, params=params).get('id'))

    # 根据自动化专用账户统一清理用例
    def clear_case(self):
        # 查询由测试账号创建的所有用例id
        case_ids = []
        query_sql = "SELECT id FROM test_plat.tp_case WHERE creator_id = %s;"
        for user_id in self.ids:
            case_ids.extend([item.get('id') for item in self.query_many(query_sql, user_id)])

        # 删除用例信息，先删除用例详情，在删除基本信息
        delete_sql = ['DELETE FROM test_plat.tp_case_detail WHERE case_id = %s;',
                      'DELETE FROM test_plat.tp_case WHERE id = %s;', ]

        for sql in delete_sql:
            self.execute_many(sql, case_ids)

    # 根据自动化专用账户统一清理测试任务
    def clear_job(self):
        # 查询由测试账号创建的所有用例id
        job_ids = []
        query_sql = "SELECT id FROM test_plat.tp_job WHERE create_user_id = %s;"
        for user_id in self.ids:
            job_ids.extend([item.get('id') for item in self.query_many(query_sql, user_id)])

        # 删除任务
        delete_sql = ['DELETE FROM test_plat.tp_job_case WHERE job_id = %s;',
                      'DELETE FROM test_plat.tp_job_tester WHERE job_id = %s;',
                      'DELETE FROM test_plat.tp_job WHERE id = %s;']

        for sql in delete_sql:
            self.execute_many(sql, job_ids)


class ClearTestPlat(ClearDB):
    """
    清理test_plat具体类
    """

    def __init__(self, env):
        super(ClearTestPlat, self).__init__(TestPlat, env)

    # 实现具体的清理过程
    def clear(self) -> None:
        self.instance.clear_job()
        self.instance.clear_case()


if __name__ == '__main__':
    db = TestPlat('dev')
    db.clear_job()
