import json
import re
from importlib import import_module

import jsonpath

from conf import HOSTS
from utils.suport.exception import CaseStepsError, SourceDataError
from utils.suport.logger import logger
from utils.suport.simulate import FakerData
from utils.tools.file import get_case_info


def __assemble_dynamic_data(data):
    """
    为用例写入动态数据
    :param data:
    :return:
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


def assemble(request) -> list:
    """
    为用例API构建测试数据
    :param request: pytest request对象
    :return: 加工后的json文件数据 [dict, dict, ...]
    """
    # 记录一下日志，开始组装测试数据也就意味着测试开始了
    logger.info("====================分割线====================")
    logger.info(f"开始测试 - {request.param}")

    # 获取测试相关信息
    case_id = request.param
    yaml_path = request.module.__file__.replace('.py', '.yaml')
    server = yaml_path.split("/tests/")[1].split("/")[0]
    env = request.config.getoption("env")

    # 用例测试步骤
    steps = get_case_info(yaml_path, case_id).get("steps", None)
    if steps is None:
        raise CaseStepsError(f"用例 {case_id} 信息详情中没有 steps 属性")

    # 每个用例可能有多个接口，同一保存到列表中
    api_origin_list = []
    api_list = []

    # 根据测试步骤从基础数据中获取需要的接口数据
    source_data = getattr(request.config, server)
    for stage in steps:
        api_data = jsonpath.jsonpath(source_data, "$." + stage)
        if not api_data:
            raise SourceDataError(f"服务 {server} 的测试数据中未找到接口 {stage} 相关信息")
        api_origin_list.append((stage.split(".", 1)[0], api_data[0]))

    # 导入API模块
    api_module = import_module("libs.api." + server)

    # 组装基础数据，将其组装成可执行数据
    for api_name, api_data in api_origin_list:
        # 获取 api 信息
        api_info = getattr(api_module, api_name)
        # 拼接 url，保存请求方式
        api_data['url'] = HOSTS[server][env] + api_info.get('route')
        api_data['method'] = api_info.get('method')
        # 检查请求头，默认 "Content-Type": "application/json;charset=UTF-8"
        if 'headers' in api_info:
            api_data['headers'] = api_info.get('headers')
        else:
            api_data['headers'] = {"Content-Type": "application/json;charset=UTF-8"}

        # 生成动态数据
        api_list.append((api_name, __assemble_dynamic_data(api_data)))

    # 如果 api_list 长度为 1，表示为 单接口 用例
    return api_list
