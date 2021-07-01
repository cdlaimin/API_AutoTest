import os
import re
import shutil

from allure import dynamic

from conf import settings
from libs.exception import DirectoryPathNotExist
from libs.logger import logger
from utils.common.file_action import get_case_info_by_id, get_case_info_by_path


def collect_item_info(item):
    """动态收集用例信息"""

    yaml_path = item.module.__file__.replace('.py', '.yaml')
    case_name = item.name
    case_id = re.findall("\\[(.+?)\\]", case_name)[0]

    # 获取用例信息
    if case_id:
        case_info = get_case_info_by_id(yaml_path, case_id)
    else:
        case_info = get_case_info_by_path(yaml_path, case_name)

    if case_info:
        # 开始写入用例信息
        dynamic.feature(case_info.get('model'))
        dynamic.story(case_info.get('func'))
        dynamic.title(case_info.get('name'))
        dynamic.description(case_info.get('description'))
        level = case_info.get('level')
        if level == 'H':
            dynamic.severity('critical')
        if level == 'M':
            dynamic.severity('normal')
        if level == 'L':
            dynamic.severity('minor')
    else:
        logger.warning(f'用例：{case_name} 信息不存在，请检查！')


def categories_to_allure():
    """
    把allure分类信息的json配置文件，放到allure测试结果文件所在目录
    :return:
    """
    category_file_path = os.path.join(settings.BASE_URL, 'conf', 'categories.json')
    allure_report_path = os.path.join(settings.BASE_URL, 'allure_results')

    if os.path.exists(allure_report_path):
        shutil.copyfile(category_file_path, allure_report_path)
    else:
        logger.warning(f'倒入用例分类信息失败！error: {DirectoryPathNotExist}')


