# -*- coding: utf-8 -*-
#
# 自动生成测试用例的模板集
#
# author: zhangjian
#
# date: 2021-07-12

FLOW_BASE = '''
import os

import allure

from conf.settings import BASE_DIR
from utils.tools.request import Requests
from utils.test.verification import verification


class class_name:
    """
    flow执行文件。
    执行函数命名方式：test_step_ + 两位序号
    """
    def __init__(self, params):
        self.Requests = Requests
        self.verification = verification

        for key, value in params.items():
            self.__setattr__(key, value)
'''

FLOW_STEP_HEAD = '''
    @allure.step(step_name)
    def test_steps(self):    
'''

FLOW_STEP_CONTENT = '''
        expect = self.steps.pop('expect')
        response = self.Requests(**self.steps).requests()
    
        # 验证结果
        self.verification(expect, response)
'''

IMAGE = '''
        # 构建上传文件参数
        image_path = os.path.join(BASE_DIR, 'static', 'image', 'head.jpeg')
        files = {"file": ("head.jpeg", open(image_path, 'rb'), 'image/jpeg')}
'''


SINGLE_API_PY = '''
import pytest

from utils.tools.request import Requests
from utils.test.verify import verification


def test_case_name(fixtures):
    expect = fixture.pop('expect')
    response = Requests(**fixture).requests()

    # 验证结果
    verification(expect, response)


if __name__ == '__main__':
    pytest.main(['-s'])
'''


MULTI_API_PY = '''
import pytest


def test_case_name(fixture):
    for func in fixture:
        func()


if __name__ == '__main__':
    pytest.main(['-s'])
'''

YAML_HEAD = '''
version: v1.0
owner: jian.z
create_time: 2021-07-26
'''