import json
import re
from importlib import import_module

import pytest

from conf.config import APP_CONFIG
from conf.settings import DISABLE_ITEMS
from utils.libs.logger import logger
from utils.action.document import get_case_data
from utils.libs.data import DynamicData, MdData, TsData


def assemble_url(data):
    """
    给测试数据组装IP和PORT
    :param data:
    :return:
    """
    app = data.get('app')
    ip = APP_CONFIG.get(app).get('ip')
    port = APP_CONFIG.get(app).get('port')

    data = json.dumps(data)  # 把字典转换成json
    # 替换ip
    data = data.replace(r'{ip}', ip)

    # 替换端口。处理特殊端口80
    if port == '80':
        data = data.replace(r':{port}', '')
    else:
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
            # 判断function是否存在。后续可根据data模块内部新增类继续扩展
            function = getattr(DynamicData, func_name, None) or getattr(MdData, func_name, None) \
                       or getattr(TsData, func_name, None)
            if function:
                instead_data = function()
                # 替换数据
                if type(instead_data) == str:
                    json_data = re.sub(f'\\$\\${func_name}', instead_data, json_data)
                if type(instead_data) == int:
                    json_data = re.sub(f'\"\\$\\${func_name}\"', str(instead_data), json_data)
            else:
                raise AttributeError(f'方法:{func_name} 不存在。')

    # strict=False 解决报错：json.decoder.JSONDecodeError: Invalid control character...
    # 原因：json.loads报错的原因，就是这个字符data数据包含了\n,\r，tab键，特殊字符 等
    return json.loads(json_data, strict=False)


def build_test_params(request):
    """
    为单接口构建测试数据
    :param request: pytest request对象
    :return: 加工后的json文件数据  dict
    """
    case_id = request.param
    json_path = request.module.__file__.replace('.py', '.json')

    # 构造测试数据，返回给用例开始执行
    logger.info(f'执行用例：{case_id}')

    # 判断用例是否已经弃用
    if case_id in DISABLE_ITEMS:
        pytest.skip(f'用例: {case_id} 已失效，跳过不执行')
    # 通过用例id获取测试数据
    data = get_case_data(json_path, case_id)
    # 添加ip
    data = assemble_url(data)
    # 添加数据
    data = assemble_data(data)

    return data


def build_test_flow(request):
    """
    为多接口流程用例构建测试数据
    :param request: pytest request对象
    :return: 包含流程中具体step函数名的list
    """
    # 先调用build_test_params完成对json数据的组装
    data = build_test_params(request)

    # 找到flow文件路径。其路径结构和tests路径结构保持一致。一个用例文件夹对应一个flow的py文件
    flow_name = re.findall("test_(.+?)_[0-9]+", request.param)[0]
    flow_path = re.sub("/[a-zA-Z_]+/[a-zA-Z_]+\\.py", f"/{flow_name}", request.module.__file__)

    module_path = 'flow' + flow_path.replace('/', '.').rsplit('tests', 1)[1]

    # 从flow文件中导入流程类。类名和flow文件名一致
    try:
        flow_module = import_module(module_path)
        flow_class = getattr(flow_module, flow_name)
    except Exception as e:
        raise e

    # 实例化类
    flow_object = flow_class(data)

    # 获取需要执行的函数名称列表
    func_list = list(filter(lambda func: re.match('test_', func), dir(flow_class)))

    # 将实例化对象的函数组装成可执行的函数列表
    exec_list = list(map(lambda func: getattr(flow_object, func), func_list))

    return exec_list


if __name__ == '__main__':
    assemble_url('aa')
