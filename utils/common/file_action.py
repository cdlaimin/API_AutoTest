import configparser
import json
import os

import yaml
import jsonpath

from conf import settings


def read_json_file(filepath):
    """
    读取json文件
    :param filepath:
    :return: dict
    """
    with open(filepath, 'r', encoding='utf8') as fp:
        data = json.load(fp)
    return data


def write_json_file(filepath, content):
    """
    写入json文件
    :param filepath:
    :param content:
    :return:
    """


def read_yaml_file(filepath):
    """
    读取yaml文件
    :param filepath:
    :return: dict
    """
    with open(filepath, 'rb') as fp:
        data = yaml.safe_load(fp)
    return data


def write_yaml_file(filepath, content):
    """
    写入yaml文件
    :param filepath:
    :param content:
    :return:
    """


def read_ini_file(filename):
    """
    固定读取conf文件夹里面的配置文件，传入文件名即可
    :return: dict
    """
    filepath = os.path.join(settings.BASE_URL, 'conf', filename)
    reader = configparser.ConfigParser()
    reader.read(filepath, encoding='utf8')

    ini_dict = {}
    for section in reader.sections():
        section_dict = {}
        for option in reader.options(section):
            section_dict.setdefault(option, reader.get(section, option))
        ini_dict.setdefault(section, section_dict)

    return ini_dict


def get_case_id(filepath, case_name):
    """
    获取用例下面的多个caseId
    :param filepath:
    :param case_name:
    :return: list => [id, id, id]
    """
    case_id = jsonpath.jsonpath(read_yaml_file(filepath), f"$.case_info..[?(@.path == '{case_name}')]..id")
    return case_id


def get_case_info_by_id(filepath, case_id):
    """
    获取用例ID对应的用例描述信息
    :param filepath:
    :param case_id:
    :return: dict
    """
    case_info = jsonpath.jsonpath(read_yaml_file(filepath), f"$.case_info..[?(@.id == '{case_id}')]")
    return case_info[0] if case_info else {}


def get_case_info_by_path(filepath, case_name):
    """
    通过用例名称获取用例描述信息
    :param filepath:
    :param case_name:
    :return: dict
    """
    case_info = jsonpath.jsonpath(read_yaml_file(filepath), f"$.case_info..[?(@.path == '{case_name}')]")
    return case_info[0] if case_info else {}


def get_case_data(filepath, case_id):
    """
    获取用例ID对应的用例测试数据
    :param filepath:
    :param case_id:
    :return:
    """
    data = read_json_file(filepath)
    return data.get(case_id)


if __name__ == '__main__':
    file_path = '/Users/zhangjian/PycharmProjects/AutoTest_MeiDuo/tests/meiduo/delivery_address/test_query_province/test_query_province.json'
    # print(read_json_file(file_path))
    # print(type(read_json_file(file_path)))
    # file_path = '/Users/zhangjian/PycharmProjects/AutoTest_MeiDuo/tests/meiduo/delivery_address/test_query_province/test_query_province.yaml'
    # print(get_case_id(file_path, 'test_query_province'))
    print(get_case_data(file_path, 'test_query_province_001'))
