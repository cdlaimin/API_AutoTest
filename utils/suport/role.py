import json

import requests

from conf import HOSTS, ACCOUNT
from utils.suport.exception import LoginError
from utils.suport.singleton import Singleton


class TestPlatRole(metaclass=Singleton):
    def __init__(self, env):
        self.host = HOSTS[env]
        self.account = ACCOUNT[env]

    def get_client(self, role):
        try:
            data = self.account[role]
        except KeyError:
            raise KeyError(f"配置文件 account.yaml 中不存在名为 {role} 的角色")
        data['type'] = "account"
        headers = {
            'Content-Type': 'application/json;'
        }
        session = requests.session()
        try:
            response = session.request(url=self.host + '/api/login/', data=json.dumps(data),
                                       method='post', headers=headers)
            if response.status_code == 200:
                token = response.json().get('token')
                session.headers['Authorization'] = 'JWT ' + token

                return session
            else:
                raise LoginError(f"账号 {data['username']} 初始化 登陆失败")
        except Exception as e:
            raise e

    @property
    def staff(self):
        return self.get_client("staff")

    @property
    def admin(self):
        return self.get_client("admin")

