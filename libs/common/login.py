import json
import requests
from loguru import logger

from conf import HOST, ACCOUNT
from utils.suport.singleton import Singleton


class TestPlat(metaclass=Singleton):
    def __init__(self, role):
        self.role = role
        self.host = HOST['test_plat']
        self.account = ACCOUNT['test_plat']

    @property
    def get_session(self):
        data = self.account[self.role]
        data['type'] = "account"
        headers = {
            'Content-Type': 'application/json;'
        }
        session = requests.session()
        try:
            response = session.request(url=self.host + '/login/', data=json.dumps(data),
                                       method='post', headers=headers)
            if response.status_code == 200:
                token = response.json().get('token')
                session.headers['Authorization'] = 'JWT ' + token
            else:
                logger.error(f"账户【{self.account[self.role]['user']}】初始化登陆失败")

        except Exception as e:
            logger.error(str(e))
            raise e

        return session
