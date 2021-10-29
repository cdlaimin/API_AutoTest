import json
import os
import re
from importlib import import_module

import pytest
from loguru import logger

from conf import HOST
from utils.suport.deceiver import FakerData
from utils.operation.file import load_json


def assemble_dynamic_data(data):
    """
    为用例写入动态数据
    :param data: dict
    :return: dict
    """
    json_data = json.dumps(data)
    # 正则匹配出需要替换的动态数据
    match_list = re.findall(r'\$\$(.+?)\"', json_data)
    if match_list:
        for func_name in set(match_list):
            # 判断function是否存在。后续可根据data模块内部新增类继续扩展
            function = getattr(FakerData, func_name, None)
            if function:
                instead_data = function()
                # 替换数据
                if isinstance(instead_data, str):
                    json_data = re.sub(f'\\$\\${func_name}', instead_data, json_data)
                if isinstance(instead_data, int):
                    json_data = re.sub(f'\"\\$\\${func_name}\"', str(instead_data), json_data)
            else:
                raise AttributeError(f'类 FakerData 中，方法: {func_name} 不存在。')

    # strict=False 不进行严格校验，解决报错：json.decoder.JSONDecodeError: Invalid control character...
    # 原因：json.loads报错的原因，就是这个字符data数据包含了\n,\r，tab键，特殊字符 等
    return json.loads(json_data, strict=False)


def build_test_data(request, target):
    """
    为单接口构建测试数据
    :param request: pytest request对象
    :param target: 测试对象
    :return: 加工后的json文件数据  dict
    """
    case_id = request.param
    json_path = request.module.__file__.replace('.py', '.json')

    # 读取测试数据
    file = load_json(json_path)
    data = file.get(case_id)

    data['url'] = HOST[target] + file['url']
    data['method'] = file['method']

    # 检查是否定制请求头
    if 'headers' in file:
        data['headers'] = file['headers']
    else:
        data['headers'] = {"Content-Type": "application/json;charset=UTF-8"}

    # 组装动态数据
    data = assemble_dynamic_data(data)

    return data


def build_test_flow(request, target):
    """
    为多接口流程用例构建测试数据
    :param request: pytest request对象
    :param target: 测试对象
    :return: 包含流程中具体step函数名的list
    """
    case_id = request.param
    json_path = request.module.__file__.replace('.py', '.json')

    # 读取测试数据
    file = load_json(json_path)
    data = file.get(case_id)

    # 组装动态数据
    data = assemble_dynamic_data(data)

    # 拼接url、拼接headers
    for key, value in data.items():
        data[key]['url'] = HOST[target] + data[key]['url']

        if 'headers' not in data[key]:
            data[key]['headers'] = {"Content-Type": "application/json;charset=UTF-8"}

    # 找到flow文件路径，在libs中
    module_path = os.path.join('libs/flow', target, request.module.__name__.rsplit('.', 1)[1].split('_', 1)[1])
    module_path = module_path.replace('/', '.')

    # 从flow文件中导入流程类。类名固定 Template
    try:
        flow_module = import_module(module_path)
        flow_class = getattr(flow_module, 'Template')
    except ModuleNotFoundError:
        logger.error(f"依赖模板文件不存在:{module_path}")
        pytest.xfail(f"依赖模板文件不存在:{module_path}")

    # 实例化类
    flow_object = flow_class(data)

    # 获取需要执行的函数名称列表
    funcs = filter(lambda func: re.match('test_', func), flow_class.__dict__)

    # 将实例化对象的函数组装成可执行的函数列表
    # exec_list = list(map(lambda func: getattr(flow_object, func), func_list))
    exec_list = [getattr(flow_object, func) for func in funcs]

    return exec_list
