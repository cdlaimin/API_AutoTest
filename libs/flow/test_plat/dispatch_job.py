import allure

from libs.sql.test_plat import DBOps
from utils.test.execute import start_test, relate
from utils.test.verify import verify


class Template:
    """模版类"""

    def __init__(self, data):
        # 加载测试步骤属性
        for key, value in data.items():
            self.__setattr__(key, value)

        # 实例化数据库操作
        self.db = DBOps()

        super().__init__()

    def __del__(self):
        # 后置
        self.db.delete_test_job_by_id(self.id)

    @allure.step("创建测试任务")
    def test_step_01(self, session):
        expect = self.step_01.pop('expect')
        response = start_test(session, self.step_01)
        # 验证结果
        verify(expect, response)

        # 获取单据id
        self.id = response.json()['data']['id']

    @allure.step("分配测试任务")
    def test_step_02(self, session):
        # 创建数据关联到第二步
        self.step_02 = relate(self.step_02, {'id': self.id})

        expect = self.step_02.pop('expect')
        response = start_test(session, self.step_02)
        # 验证结果
        verify(expect, response)
