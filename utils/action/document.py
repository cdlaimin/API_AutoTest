import configparser
import json
import os

import ruamel.yaml
import yaml
import jsonpath

from conf.settings import BASE_DIR


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
    with open(filepath, 'w', encoding='utf8') as fp:
        # 将ensure_ascii 设置为false，避免将汉字转成ascii码
        # indent 参数让json文本保持缩进格式，数字表述缩进字符数
        json.dump(content, fp, ensure_ascii=False, indent=2)


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
    with open(filepath, 'w', encoding='utf8') as fp:
        # allow_unicode参数为true时，才会进行编码。否则写入的文件都是进过url编码的
        # default_flow_style 表示dump后的字典数据全部以yml格式显示,默认为为True
        # sort_keys 不给key排序，这样能保持原来字典的顺序写入。为True时按字母的排序展示，默认为为True
        # indent 参数让yaml文本保持缩进格式。有下次，列表符号不会跟随缩进
        # yaml.safe_dump(content, fp, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=4)

        # ----为了dump保持缩进，这里采用另一个模块实现
        r_yaml = ruamel.yaml.YAML()
        r_yaml.indent(sequence=4, offset=2)
        r_yaml.dump(content, fp)


def read_ini_file(filename):
    """
    固定读取conf文件夹里面的配置文件，传入文件名即可
    :return: dict
    """
    filepath = os.path.join(BASE_DIR, 'conf', filename)
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


def get_case_info(filepath, case_id):
    """
    获取用例ID对应的用例描述信息
    :param filepath:
    :param case_id:
    :return: dict
    """
    case_info = jsonpath.jsonpath(read_yaml_file(filepath), f"$.case_info..[?(@.id == '{case_id}')]")
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
    # file_path = '/Users/zhangjian/PycharmProjects/AutoTest_MeiDuo/tests/meiduo/areas/test_query_province/test_query_province.json'
    # print(read_json_file(file_path))
    # print(type(read_json_file(file_path)))
    file_path = '/tests/meiduo/areas/test_query_province/test_query_province.yaml'
    # print(get_case_id(file_path, 'test_query_province'))
    print(get_case_data(file_path, 'test_query_province_001'))