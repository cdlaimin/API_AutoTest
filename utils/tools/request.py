import json

import requests

from conf import settings
from utils.libs.exception import LoginFailException
from utils.libs.logger import logger


class Requests:
    """封装requests模块"""

    def __init__(self, **kwargs):
        # 初始化请求session
        app = kwargs.pop('app')
        self.session = init_requests(app)
        self.kwargs = kwargs

    def requests(self):
        try:
            if self.kwargs.get('data'):
                self.kwargs['data'] = json.dumps(self.kwargs['data'])

            response = self.session.request(**self.kwargs)

            logger.info(f'请求地址:{response.request.url}')
            logger.info(f'请求方式:{response.request.method}')
            logger.info(f'请求体:{response.request.body}')

            return response
        except Exception as e:
            logger.error('接口测试失败！')
            logger.error(f'请求地址:{self.kwargs.get("url")}')
            raise e


def init_requests(app):
    # 根据测试系统获取不同的session
    if app == 'meiduo':
        return init_meiduo
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


# 单例模式。避免重复登陆
init_meiduo = init_meiduo()

if __name__ == '__main__':
    print(init_meiduo)
