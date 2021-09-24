import os
import re
import shutil
import warnings

from allure import dynamic

from conf import APP_CONFIG
from conf import BASE_DIR
from utils.libs.exception import DirectoryNotExist
from utils.libs.logger import logger
from utils.action.document import get_case_info, load_yaml


def collect_item_info(item):
    """动态收集用例信息"""

    yaml_path = item.module.__file__.replace('.py', '.yaml')
    case_full_name = item.name
    case_id = re.findall("\\[(.+?)\\]", case_full_name)[0]

    author = load_yaml(yaml_path).get('owner')
    tag = "MD" if '/meiduo/' in yaml_path else "TS"

    # 获取用例信息
    case_info = get_case_info(yaml_path, case_id)

    if case_info:
        # 开始写入用例信息
        dynamic.link(author)
        dynamic.tag(tag)
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
        warnings.warn(f'用例:{case_id} 信息不存在，请检查！')
        logger.warning(f'用例:{case_id} 信息不存在，请检查！')


def write_report_information(session):
    """
    把allure分类信息的json配置文件，放到allure测试结果文件所在目录
    创建报告环境信息，主要是写入当前测试的app信息
    :return:
    """
    category_file_path = os.path.join(BASE_DIR, 'conf', 'categories.json')
    allure_report_path = os.path.join(BASE_DIR, 'allure-results')

    if os.path.exists(allure_report_path):
        try:
            # 复制测试结果分类文件到报告目录
            shutil.copy(category_file_path, allure_report_path)

            # 写入测试app信息
            app = session.config.getoption('app')
            with open(os.path.join(allure_report_path, 'environment.properties'), 'w+', encoding='utf-8') as f:
                if app == 'all':
                    for index, app_name in enumerate(APP_CONFIG.keys()):
                        f.write(
                            f'app{index + 1}={app_name}\n'
                        )
                else:
                    f.write(
                        f'app={app}\n'
                    )
        except Exception as e:
            logger.warning(f'导入用例分类信息失败！error: {e}')
    else:
        logger.warning(f'导入用例分类信息失败！error: {DirectoryNotExist}')


if __name__ == '__main__':
    for index, app_name in enumerate(APP_CONFIG.keys()):
        print(index, app_name)
