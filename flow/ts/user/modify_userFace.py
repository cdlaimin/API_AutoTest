
import os

import allure

from conf.settings import BASE_DIR
from utils.tools.request import Requests
from utils.test.verify import verification


class modify_userFace:
    """
    flow执行文件。
    执行函数命名方式：test_step_ + 两位序号
    """
    def __init__(self, params):
        self.Requests = Requests
        self.verification = verification

        for key, value in params.items():
            self.__setattr__(key, value)

    @allure.step("上传图片")
    def test_step_01(self):    

        # 构建上传文件参数
        image_path = os.path.join(BASE_DIR, 'static', 'image', 'head.jpeg')
        files = {"file": ("head.jpeg", open(image_path, 'rb'), 'image/jpeg')}

        self.step_01['files'] = files
        expect = self.step_01.pop('expect')
        response = self.Requests(**self.step_01).requests()
    
        # 验证结果
        self.verification(expect, response)

        self.step_02['data']['picurl'] = response.json()['data']['picurl']

    @allure.step("确认提交")
    def test_step_02(self):    

        expect = self.step_02.pop('expect')
        response = self.Requests(**self.step_02).requests()
    
        # 验证结果
        self.verification(expect, response)

