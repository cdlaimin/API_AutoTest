import json
import os
import re
from copy import deepcopy

from conf.settings import BASE_DIR
from utils.action.document import read_json_file, write_json_file, read_yaml_file, write_yaml_file
from utils.libs.exception import ParamsCheckFailed, RequestMethodInvalid


def build_case(path: str, app: str, api: str, method: str, headers: dict, data: list, expect: list, args: list, fixture='params'):
    """
    构建测试用例，函数入参没有全部传入时，生成用例后，需要测试人员手动补全用例。
    同时建议新增一个用例后，调试通过在生成下一个，避免生成垃圾用例
    :param path: 必填，相对于项目根目录(BASE_DIR)的相对目录，最后一级应是用例目录
    :param api: 必填，测试API接口，以'/'结尾
    :param app: 必填，测试项目app名称
    :param method: 必填，请求方法
    :param headers: 请求头字典
    :param fixture: 夹具。可以是单个夹具，也可以是一个夹具列表(请求参数的夹具放首位)。默认值：params
    :param data: 请求参数，字典组成的列表
    :param expect: 预期结果，字典组成的列表，尽量使用字典。为列表时，预期结果要与data/params保持一一对应
    :param args: 测试用例信息，字典组成的列表，和expect顺序对应
                 [{model:"model",func:"func",case_name:"case_name",description="description",level:"level"},...]
    :return: None
    """
    # 校验必填字段
    if not all([path, api, app, method]):
        raise ParamsCheckFailed('必填字段校验失败，请检查。')
    elif method not in ['post', 'get', 'put', 'delete']:
        raise RequestMethodInvalid('请求方式不合法，请检查。')

    # 创建用例文件夹
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    # 模版路径
    temp_path = os.path.join(BASE_DIR, 'build', 'template')

    # 构建py文件
    build_py(abs_path, temp_path, fixture)

    # 构建json文件
    build_json(abs_path, temp_path, app, api, method, headers, data=data, expect=expect)

    # 构建yaml文件
    build_yaml(abs_path, temp_path, args)


def build_py(abs_path, temp_path, fixture):
    """
    构建执行PY文件
    :param abs_path: 要创建文件的目录
    :param temp_path: py模板文件目录
    :param fixture: 夹具。可以是单个夹具，也可以是一个夹具列表(请求参数的夹具放首位)。默认值：params
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 读取模版文件
    py_temp = os.path.join(temp_path, 'py_file.py')
    with open(py_temp, 'r', encoding='utf8') as pt:
        origin_content = pt.read()

    # 写入夹具信息
    if type(fixture) in (list, tuple):
        fixture_str = ', '.join(fixture)
        new_content = re.sub('fixtures', fixture_str, origin_content)
        new_content = re.sub('fixture', fixture[0], new_content)
    elif isinstance(fixture, str):
        new_content = re.sub('fixtures|fixture', fixture, origin_content)
    else:
        raise ParamsCheckFailed('参数:fixture 数据类型错误。')

    # 写入用例名称
    new_content = re.sub(r'test_case_name', case_name, new_content)

    # 生成py文件
    with open(os.path.join(abs_path, case_name, '.py'), 'w') as pn:
        pn.write(new_content)


def build_json(abs_path, temp_path, app, api, method, headers, **kwargs):
    """
    构建测试数据的json文件
    :param abs_path: 要创建文件的目录
    :param temp_path: json模板文件目录
    :param api: 测试接口api
    :param app: 测试的app
    :param method: 请求方法
    :param headers: 请求头
    :param kwargs: 包含data、expect的字典
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 读取模版文件
    json_temp = os.path.join(temp_path, 'json_file.json')
    content = read_json_file(json_temp)['test_case_number']

    # 先组装通用参数
    content['method'] = method
    content['app'] = app
    # content = json.loads(json.dumps(content).replace('{api}', api if api[-1] == '/' else api + '/'))
    content = json.loads(json.dumps(content).replace('{api}', api))

    # 根据请求方式弹出不需要的key
    if method == 'get':
        content.pop('data')
    else:
        content.pop('params')

    # 写入到json文件的内容
    json_dict = {}

    # 组装headers
    content = assemble_header(content, headers=headers)

    # 如果同时传入了data和expect那么就进入数据组装逻辑
    # 否则直接按模板生成待手工添加数据的json文件
    if all(list(kwargs.values())):
        # 组装请求数据和预期结果
        json_value = assemble_data_and_expect(content, **kwargs)

        # 组装json文件
        for index, sub_json_value in enumerate(json_value):
            json_dict[case_name + '_0' + str(index + 1)] = sub_json_value
    else:
        json_dict[case_name + '_01'] = content

    # 生成json文件
    write_json_file(os.path.join(abs_path, case_name, '.json'), json_dict)


def build_yaml(abs_path, temp_path, args):
    """
    构建包含用例信息的yaml文件
    :param abs_path:
    :param temp_path:
    :param args: 用例信息列表，[{}, {}, ...] 可以是None
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 读取模版文件
    yaml_temp = os.path.join(temp_path, 'yaml_file.yaml')
    content = read_yaml_file(yaml_temp)['case_info'][0]

    # 生成用例信息数据
    yaml_dict = {}
    value_list = []

    if args is None:
        content['id'] = case_name + '_01'
        content['path'] = case_name

        value_list.append(content)
    elif not isinstance(args, list):
        raise ParamsCheckFailed('参数:args 数据类型错误。')
    else:
        for index, sub_info in enumerate(args):
            value_list.append(deepcopy(content))
            value_list[index]['id'] = case_name + '_0' + str(index + 1)
            value_list[index]['path'] = case_name
            value_list[index]['model'] = sub_info.get('model')
            value_list[index]['func'] = sub_info.get('func')
            value_list[index]['case_name'] = sub_info.get('case_name')
            value_list[index]['description'] = sub_info.get('description')
            value_list[index]['level'] = sub_info.get('level', 'M')

    yaml_dict['case_info'] = value_list

    # 生成yaml文件
    write_yaml_file(os.path.join(abs_path, case_name, '.yaml'), yaml_dict)


def assemble_data_and_expect(content, **kwargs):
    """
    组装请求数据和预期结果
    :param content: 取自json模板请求数据字典，即test_case_number的值
    :param kwargs: 包含请求数据和预期结果的字典
    :return: list  [{}, {}, {}..]
    """
    # 先找出请求中用什么参数的key
    if 'data' in content:
        key = 'data'
    elif 'params' in content:
        key = 'params'
    else:
        raise ParamsCheckFailed('json模板数据类型错误，请联系管理员。')

    if isinstance(kwargs['data'], list) and isinstance(kwargs['expect'], list):
        if len(kwargs['data']) != len(kwargs['expect']):
            raise ParamsCheckFailed('检查data和expect列表长度是否一致')
        request_list = []
        for index, (data, expect) in enumerate(zip(kwargs['data'], kwargs['expect'])):
            request_list.append(deepcopy(content))
            request_list[index][key] = data
            request_list[index]['expect'] = expect
        return request_list
    else:
        raise ParamsCheckFailed('参数:data或expect 数据类型错误。')


def assemble_header(content, headers):
    """
    组装请求头
    :param content: 取自json模板请求数据字典，即test_case_number的值
    :param headers: 请求头字典
    :return:
    """
    if headers:
        content['headers'] = headers
    else:
        content['headers'] = {
            "Content-Type": "application/json"
        }

    return content
