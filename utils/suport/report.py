import os
import re
import shutil

from allure import dynamic
from loguru import logger

from conf import BASE_DIR
from utils.suport.exception import DirectoryNotExist
from utils.tools.file import get_case_info, load_yaml


def collect_item_info(item):
    """动态收集用例信息"""

    yaml_path = item.module.__file__.replace('.py', '.yaml')
    case_full_name = item.name
    case_id = re.findall("\\[(.+?)\\]", case_full_name)[0]
    author = load_yaml(yaml_path).get('owner')

    # 获取用例信息
    case_info = get_case_info(yaml_path, case_id)

    if case_info:
        # 开始写入用例信息
        dynamic.link(author)
        dynamic.title(case_info.get('CaseName'))
        dynamic.description(case_info.get('desc'))
        priority = case_info.get('priority')
        if priority == '高':
            dynamic.severity('critical')
        if priority == '中':
            dynamic.severity('normal')
        if priority == '低':
            dynamic.severity('minor')
    else:
        logger.warning(f'用例:{case_id} 信息不存在，请检查！')


def write_report_information(session):
    """
    把allure分类信息的json配置文件，放到allure测试结果文件所在目录
    创建报告环境信息，主要是写入当前测试的app信息
    :return:
    """
    category_file_path = os.path.join(BASE_DIR, 'static', 'allure', 'categories.json')
    allure_report_path = os.path.join(BASE_DIR, 'allure-results')

    if os.path.exists(allure_report_path):
        try:
            # 复制测试结果分类文件到报告目录
            shutil.copy(category_file_path, allure_report_path)

            # 写入测试app信息
            target = session.config.getoption('target')
            with open(os.path.join(allure_report_path, 'environment.properties'), 'w+', encoding='utf-8') as f:
                pass
        except Exception as e:
            logger.warning(f'导入用例分类信息失败！error: {e}')
    else:
        logger.warning(f'导入用例分类信息失败！error: {DirectoryNotExist}')


