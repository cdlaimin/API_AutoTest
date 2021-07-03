import json
import re

import pytest

from conf import settings
from libs.logger import logger
from utils.common.file_action import get_case_data
from utils.tools.init_data import DynamicData, StaticData


def assemble_url(data):
    """
    给测试数据组装IP和PORT
    :param data:
    :return:
    """
    app = data.get('app')
    ip = settings.APP_CONFIG.get(app).get('ip')
    port = settings.APP_CONFIG.get(app).get('port')

    data = json.dumps(data)  # 把字典转换成json
    # 替换ip和端口
    data = data.replace(r'{ip}', ip)
    data = data.replace(r'{port}', port)

    # 重新转回字典并返回
    return json.loads(data, strict=False)


def assemble_data(data):
    """
    为用例写入动态数据
    :param data: dict
    :return: dict
    """
    json_data = json.dumps(data)
    # 正则匹配出需要替换的动态数据
    match_list = re.findall(r'\$\$(.+?)\"', json_data)
    if match_list:
        for func_name in list(set(match_list)):
            # 判断function是否存在
            if hasattr(DynamicData, func_name):
                function = getattr(DynamicData, func_name)
                instead_data = function()

                # 替换数据
                if type(instead_data) == str:
                    json_data = re.sub(f'\\$\\${func_name}', instead_data, json_data)
                if type(instead_data) == int:
                    json_data = re.sub(f'\"\\$\\${func_name}\"', str(instead_data), json_data)
            else:
                raise AttributeError(f'函数{func_name}不存在，请检查！')

    # 正则匹配出需要替换的静态数据
    match_list = re.findall(r'##(.+?)\"', json_data)
    if match_list:
        for func_name in list(set(match_list)):
            # 判断function是否存在
            if hasattr(StaticData, func_name):
                function = getattr(StaticData, func_name)
                instead_data = function()
                # 替换数据
                if type(instead_data) == str:
                    json_data = re.sub(f'##{func_name}', instead_data, json_data)
                if type(instead_data) == int:
                    json_data = re.sub(f'\"##{func_name}\"', str(instead_data), json_data)
            else:
                raise AttributeError(f'函数{func_name}不存在，请检查！')

    # strict=False 解决报错：json.decoder.JSONDecodeError: Invalid control character...
    # 原因：json.loads报错的原因，就是这个字符data数据尽量包含了\n,\r，tab键，特殊字符 等
    return json.loads(json_data, strict=False)


def build_test_data(request):
    """
    构造测试数据
    :param data:
    :return:
    """
    case_id = request.param
    json_path = request.module.__file__.replace('.py', '.json')

    # 构造测试数据，返回给用例开始执行
    logger.info(f'=====执行用例：{case_id}=====')

    # 判断用例是否已经弃用
    if case_id in settings.DISABLE_ITEMS:
        pytest.skip(f'用例: {case_id} 已失效，跳过不执行')
    # 通过用例id获取测试数据
    data = get_case_data(json_path, case_id)
    # 添加ip
    data = assemble_url(data)
    # 添加数据
    data = assemble_data(data)

    return data


if __name__ == '__main__':
    assemble_url('aa')
