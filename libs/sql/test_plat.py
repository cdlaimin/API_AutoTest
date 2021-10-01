from utils.suport.singleton import Singleton
from utils.operate.database import DataBase


class DBOps(DataBase, metaclass=Singleton):
    """数据库相关操作"""

    def __init__(self):
        super().__init__('test_plat')

    # 根据自动化专用账户统一清理用例
    def delete_case_by_id(self):
        sql_list = ['delete from test_plat.tp_case_detail where case_id = %s;',
                    'delete from test_plat.tp_case where id = %s;', ]

        user_ids = [item['id'] for item in self.account.values()]

        for user_id in user_ids:
            query_set = self.get_cases_by_user(user_id)
            if query_set:
                ids = [item['id'] for item in query_set]
                for sql in sql_list:
                    self.execute_many(sql, ids)

    # 查询用户创建的多条用例信息
    def get_cases_by_user(self, user_id):
        sql = f'select * from test_plat.tp_case where creator_id = {user_id}'
        return self.query_many(sql)

    # 根据测试任务ID 删除 测试任务
    def delete_test_job_by_id(self, job_id):
        sql_list = [f'DELETE FROM test_plat.tp_job_case where job_id = {job_id};',
                    f'DELETE FROM test_plat.tp_job_tester where job_id = {job_id};',
                    f'DELETE FROM test_plat.tp_job where id = {job_id};']

        for sql in sql_list:
            self.execute_one(sql)
