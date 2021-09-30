import os
import re

from build.template import templates
from build.template.templates import YAML_HEAD
from conf import BASE_DIR
from utils.operate.document import load_json, dump_yaml


def build_case(path, fixture, json: list, yaml: list):
    """
    构建测试用例，函数入参没有全部传入时，生成用例后，需要测试人员手动补全用例。
    同时建议新增一个用例后，调试通过在生成下一个，避免生成垃圾用例
    :param path: 必填，相对于项目根目录(BASE_DIR)的相对目录，最后一级应是用例目录
    :param fixture: 必填，夹具。可以是单个夹具，也可以是一个夹具列表(请求参数的夹具放首位)
    :param json: 必填，测试数据集
    :param yaml: 必填，用例信息集
    :return: None
    """
    # 校验必填字段
    if not all([path, fixture, json, yaml]):
        raise ValueError('必填字段校验失败，请检查。')

    # 创建用例文件夹
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    # 构建py文件
    build_py(abs_path, fixture)

    # 构建json文件
    build_json(abs_path, fixture, json)

    # 构建yaml文件
    build_yaml(abs_path, yaml)


def build_py(abs_path, fixture):
    """
    构建执行PY文件
    :param abs_path: 要创建文件的目录
    :param fixture: 夹具。可以是单个夹具，也可以是一个夹具列表(请求参数的夹具放首位)。默认值：params
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 读取模版文件
    if 'suport' in fixture:
        origin_content = templates.MULTI_API_PY

    else:
        origin_content = templates.SINGLE_API_PY

    # 写入夹具信息
    if type(fixture) in (list, tuple):
        fixture_str = ', '.join(fixture)
        new_content = re.sub('fixtures', fixture_str, origin_content)
        new_content = re.sub('fixture', fixture[0], new_content)
    elif isinstance(fixture, str):
        new_content = re.sub('fixtures|fixture', fixture, origin_content)
    else:
        raise ValueError('参数:fixture 数据类型错误。')

    # 写入用例名称
    new_content = re.sub(r'test_case_name', case_name, new_content)

    # 生成py文件
    with open(os.path.join(abs_path, case_name + '.py'), 'w', encoding='utf8') as pn:
        pn.write(new_content)


def build_json(abs_path, fixture, json):
    """
    构建测试数据的json文件
    :param abs_path: 要创建文件的目录
    :param fixture: 夹具
    :param json: 用例数据列表
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 先组装通用参数
    # content = json.loads(json.dumps(content).replace('{api}', api if api[-1] == '/' else api + '/'))

    # 写入到json文件的内容
    json_dict = dict()

    # 根据夹具来决定json数据文件的组装方式
    if all([json, isinstance(json, list)]):
        # 组装json文件，根据夹具决定拼接方式
        if 'suport' in fixture:
            # 组装json文件时，同步完成flow文件的步骤文件
            class_name = case_name.split('_', 1)[1]
            # 生成flow步骤py文件
            flow_path = abs_path.rsplit('/', 1)[0].replace('/tests/', '/suport/')
            # 检查目录路径是否存在，不存在则创建
            if not os.path.exists(flow_path):
                os.makedirs(flow_path)
            # 写入文件
            file = os.path.join(flow_path, class_name + '.py')
            with open(file, 'w', encoding='utf8') as fp:
                base_content = templates.FLOW_BASE.replace('class_name', class_name)
                fp.write(base_content)

            # json数据组装
            temp_dict = dict()
            for index, sub_json in enumerate(json):
                # flow逻辑
                step = sub_json.pop('step')
                write_flow_file(file, step, index)

                temp_dict['step_0' + str(index + 1)] = sub_json
            json_dict[case_name + '_01'] = temp_dict
        else:
            for index, sub_json in enumerate(json):
                json_dict[case_name + '_0' + str(index + 1)] = sub_json
    else:
        raise ValueError('参数:json 数据类型错误。')

    # 生成json文件
    load_json(os.path.join(abs_path, case_name + '.json'), json_dict)


def write_flow_file(file, step, index):
    """
    写入测试步骤
    :param file:
    :param step:
    :param index:
    :return:
    """
    # 调用本函数，step为空时引发异常
    if not step:
        raise ValueError('参数:step 数据错误。')

    with open(file, 'a', encoding='utf8') as fp:
        # 头部
        head_content = templates.FLOW_STEP_HEAD
        head_content = head_content.replace('steps', 'step_0' + str(index + 1))
        head_content = head_content.replace('step_name', f'"{step.get("name")}"')

        fp.write(head_content)

        # 检查是否有setup
        if step.get('setup'):
            for content in step['setup']:
                if hasattr(templates, content):
                    fp.write(getattr(templates, content) + '\n')
                else:
                    fp.write("        " + content + '\n')

        body_content = templates.FLOW_STEP_CONTENT
        body_content = body_content.replace('steps', 'step_0' + str(index + 1))

        fp.write(body_content + '\n')

        # 检查是否有teardown
        if step.get('teardown'):
            for content in step['teardown']:
                if hasattr(templates, content):
                    fp.write(getattr(templates, content))
                else:
                    fp.write("        " + content + '\n')


def build_yaml(abs_path, yaml):
    """
    构建包含用例信息的yaml文件
    :param abs_path:
    :param yaml: 用例信息列表，[{}, {}, ...] 可以是None
    :return:
    """
    # 获取case_name
    case_name = abs_path.rsplit('/', 1)[1]

    # 生成用例信息数据
    yaml_dict = dict()
    value_list = []
    # 获取模板数据
    for item in YAML_HEAD.split('\n'):
        if item:
            key, value = item.split(':')
            yaml_dict[key.strip()] = value.strip()

    if yaml is None:
        content = dict()
        content['id'] = case_name + '_01'
        content['path'] = case_name

        value_list.append(content)
    elif not isinstance(yaml, list):
        raise ValueError('参数:yaml 数据类型错误。')
    else:
        for index, sub_info in enumerate(yaml):
            content = dict()
            content['id'] = case_name + '_0' + str(index + 1)
            content['path'] = case_name
            content['model'] = sub_info.get('model')
            content['func'] = sub_info.get('func')
            content['case_name'] = sub_info.get('case_name')
            content['description'] = sub_info.get('description')
            content['level'] = sub_info.get('level', 'M')

            value_list.append(content)

    yaml_dict['case_info'] = value_list

    # 生成yaml文件
    dump_yaml(os.path.join(abs_path, case_name + '.yaml'), yaml_dict)


if __name__ == '__main__':
    yaml_dict = dict()
    # 获取模板数据
    for item in YAML_HEAD.split('\n'):
        if item:
            key, value = item.split(':')
            yaml_dict[key.strip()] = value.strip()

    print(yaml_dict)
