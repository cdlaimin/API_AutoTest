import json

import requests

from conf import settings
from utils.libs.exception import LoginFailException
from utils.libs.logger import logger
from utils.tools.data import TsData, DynamicData
from utils.tools.helper import api_logger


class Requests:
    """封装requests模块"""

    def __init__(self, **kwargs):
        # 初始化请求session
        self.app = kwargs.pop('app')
        self.session = init_requests(self.app)
        self.kwargs = kwargs

    @api_logger
    def requests(self):
        """发起请求，返回响应对象"""
        # ts是php开发的前后端不分离系统，比较特殊
        if self.kwargs.get('data') and self.app != 'ts':
            self.kwargs['data'] = json.dumps(self.kwargs['data'])

        response = self.session.request(**self.kwargs)
        return response


def init_requests(app):
    # 根据测试系统获取不同的session
    if app == 'meiduo':
        return init_meiduo
    if app == 'ts':
        return init_ts
    # 扩展其他系统初始化信息


def init_meiduo():
    """美多商城初始化"""
    session = requests.session()
    host = settings.APP_CONFIG.get('meiduo').get('ip')
    port = settings.APP_CONFIG.get('meiduo').get('port')

    url = 'http://' + host + ':' + port + '/login/'
    method = 'post'
    data = {
        'username': 'zhangjian',
        'password': 'Zj123456'
    }
    # 登陆系统
    response = session.request(method=method, url=url, data=data)
    if response.status_code == 200:
        # 添加身份认证信息
        session.headers['Authorization'] = 'JWT ' + response.json().get('token')
        return session
    logger.warning('美多商城初始化登陆失败')
    raise LoginFailException


def init_ts():
    """
    thinkSNS初始化
    :return:
    """
    session = requests.session()
    host = settings.APP_CONFIG.get('ts').get('ip')
    port = settings.APP_CONFIG.get('ts').get('port')

    if port == '80':
        url = 'http://' + host + '/thinksns/index.php?app=public&mod=Passport&act=doLogin'
        headers = {
            "Referer": 'http://' + host + '/thinksns/',
        }
    else:
        url = 'http://' + host + ':' + port + '/thinksns/index.php?app=public&mod=Passport&act=doLogin'
        headers = {
            "Referer": 'http://' + host + ':' + port + '/thinksns/',
        }

    method = 'post'
    data = {
        "login_email": TsData.user_email(),
        "login_password": DynamicData.const_password(),
        "login_remember": 0
    }
    # 登陆系统
    response = session.request(method=method, url=url, data=data, headers=headers)
    if response.status_code == 200 and response.json()['status'] == 1:
        return session
    logger.warning('ThinkSNS初始化登陆失败')
    raise LoginFailException


# 单例模式。避免重复登陆
init_meiduo = init_meiduo()
init_ts = init_ts()

if __name__ == '__main__':
    print(init_ts)
