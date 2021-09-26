import json
import os
import sys

import gevent
import requests

from utils.libs.logger import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf.settings import BASE_DIR
from conf.config import APP_CONFIG, UPLOADED_CASES


from utils.operate.document import read_yaml_file, write_yaml_file
from utils.libs.notice import send_upload_result_to_wechat


# 用例信息列表，每一个item即为一条用例信息
case_list = list()


def get_case_path(dir_name):
    """
    获取用例路径
    :param dir_name: 需要收集用例的目录。给予项目根目录的相对路径
    :return: list
    """
    dir_full_name = os.path.join(BASE_DIR, dir_name)
    path_list = list()

    for path, dirs, files in os.walk(dir_full_name):
        for file in files:
            if file.endswith('.yaml'):
                path_list.append(os.path.join(path, file))

    return path_list


def collect_case_info(case_path):
    """
    收集用例信息
    :param case_path: 用例路径
    :return:
    """
    data = read_yaml_file(case_path)

    version = data.get('version')
    owner = data.get('owner')
    create_time = data.get('create_time')

    for case in data.get('case_info'):
        # 判断是否已经上传
        case_id = case.get('id')
        if case_id not in UPLOADED_CASES['case_list']:
            info = dict()
            info['case_id'] = case_id
            info['exec_path'] = case_path.replace('.yaml', '.py').split('tests/')[-1] + "::" + case.get('path')
            info['client'] = case.get('model')
            info['module'] = case.get('func')
            info['case_name'] = case.get('case_name')
            info['description'] = case.get('description')
            info['level'] = case.get('level')

            info['version'] = version
            info['owner'] = owner
            info['add_time'] = create_time

            # 从此脚本收集的用例全部是自动化用例
            info['is_auto'] = True

            # 添加到上传列表
            case_list.append(info)


def async_collect(dir_path="tests"):
    """
    考虑到上传时会有大批量的用例需要同步，这里采用协程异步收集
    :param dir_path: 需要收集用例的目录。给予项目根目录的相对路径
    :return:
    """
    tasks = [gevent.spawn(collect_case_info, case_path) for case_path in get_case_path(dir_path)]
    gevent.joinall(tasks)


def upload_case():
    # 登陆获取token
    app = APP_CONFIG.get('test_plat')
    login_host = 'http://' + app.get('ip') + ':' + app.get('port') + '/login/'
    user = {
        "username": sys.argv[1],
        "password": sys.argv[2],
        'type': 'account'
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url=login_host, data=json.dumps(user), headers=headers)
    except Exception:
        raise Exception('上传用例，前置登陆异常')
    else:
        if response.status_code == 200:
            token = response.json().get('token')
        else:
            raise Exception(f'上传用例，前置登陆失败。详情:{response.text}')

    # 组装上传接口的header
    headers['Authorization'] = 'JWT ' + token
    upload_host = 'http://' + app.get('ip') + ':' + app.get('port') + '/uploadManyCase/'

    if case_list:
        try:
            response = requests.post(url=upload_host, data=json.dumps({'data': case_list}), headers=headers)
        except Exception:
            raise Exception('用例上传API异常')
        else:
            if response.status_code == 200:
                result = response.json()
                # 发送结果到企微
                send_upload_result_to_wechat(**result)
            else:
                logger.error(f'上传用例接口调用失败。详情:{response.text}')
                raise Exception(f'上传用例接口调用失败。详情:{response.text}')

        # 记录已经上传成功的用例
        UPLOADED_CASES['case_list'] = UPLOADED_CASES['case_list'] + result['success']
        path = os.path.join(BASE_DIR, 'conf', 'uploaded_case.yaml')
        write_yaml_file(path, UPLOADED_CASES)
    else:
        logger.warning(f'warning:用例列表[case_list]为空')


if __name__ == '__main__':
    # 执行文件时，依次传入 用户名 密码 收集目录
    async_collect(sys.argv[3])
    upload_case()

