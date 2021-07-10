import os
import re
import shutil

from allure import dynamic

from conf import settings
from utils.libs.exception import DirectoryPathNotExist
from utils.libs.logger import logger
from utils.action.document import get_case_info


def collect_item_info(item):
    """动态收集用例信息"""

    yaml_path = item.module.__file__.replace('.py', '.yaml')
    case_full_name = item.name
    case_id = re.findall("\\[(.+?)\\]", case_full_name)[0]

    # 获取用例信息
    case_info = get_case_info(yaml_path, case_id)

    if case_info:
        # 开始写入用例信息
        dynamic.feature(case_info.get('model'))
        dynamic.story(case_info.get('func'))
        dynamic.title(case_info.get('case_name'))
        dynamic.description(case_info.get('description'))
        level = case_info.get('level')
        if level == 'H':
            dynamic.severity('critical')
        if level == 'M':
            dynamic.severity('normal')
        if level == 'L':
            dynamic.severity('minor')
    else:
        logger.warning(f'用例:{case_id} 信息不存在，请检查！')


def categories_to_allure():
    """
    把allure分类信息的json配置文件，放到allure测试结果文件所在目录
    :return:
    """
    category_file_path = os.path.join(settings.BASE_DIR, 'conf', 'categories.json')
    allure_report_path = os.path.join(settings.BASE_DIR, 'allure-results')

    if os.path.exists(allure_report_path):
        try:
            shutil.copy(category_file_path, allure_report_path)
        except Exception as e:
            logger.warning(f'导入用例分类信息失败！error: {e}')
    else:
        logger.warning(f'导入用例分类信息失败！error: {DirectoryPathNotExist}')


