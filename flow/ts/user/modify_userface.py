import os

import allure

from conf.settings import BASE_DIR


class ModifyUserface:
    def __init__(self, params, Requests, verification):
        self.upload_params = params['upload_image']
        self.submit_params = params['submit']
        self.Requests = Requests
        self.verification = verification

    @allure.step('上传图片')
    def upload_image(self):
        """上传头像"""

        # 构建上传文件参数
        image_path = os.path.join(BASE_DIR, 'static', 'image', 'head.jpeg')
        files = {"file": ("head.jpeg", open(image_path, 'rb'), 'image/jpeg')}

        self.upload_params['files'] = files

        expect = self.upload_params.pop('expect')
        response = self.Requests(**self.upload_params).requests()

        # 验证结果
        self.verification(expect, response)

        # 为确认提交拼接参数
        self.submit_params['data']['picurl'] = response.json()['data']['picurl']

    @allure.step('确认提交')
    def submit(self):
        """确认提交"""
        expect = self.submit_params.pop('expect')
        response = self.Requests(**self.submit_params).requests()
        # 验证结果
        self.verification(expect, response)
