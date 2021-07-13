import os

import allure

from conf.settings import BASE_DIR
from utils.tools.request import Requests
from utils.test.verification import verification


class create_microBar:
    """
    flow执行文件。
    执行函数命名方式：test_step_ + 两位序号
    """
    def __init__(self, params):
        self.Requests = Requests
        self.verification = verification

        for key, value in params.items():
            self.__setattr__(key, value)

    # 注释上边的代码固定不变；下方代码根据不同的flow具体改变
    @allure.step('上传微吧LOGO')
    def test_step_01(self):
        # 构建上传文件参数
        image_path = os.path.join(BASE_DIR, 'static', 'image', 'head.jpeg')
        files = {"file": ("head.jpeg", open(image_path, 'rb'), 'image/jpeg')}

        self.step_01['files'] = files

        expect = self.step_01.pop('expect')
        response = self.Requests(**self.step_01).requests()

        # 验证结果
        self.verification(expect, response)

    @allure.step('提交微吧基本信息')
    def test_step_02(self):
        expect = self.step_02.pop('expect')
        response = self.Requests(**self.step_02).requests()

        # 验证结果
        self.verification(expect, response)
