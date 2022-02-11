import os
import re
import shutil
from datetime import datetime

from allure import dynamic

from conf import BASE_DIR, HOSTS
from utils.suport import logger
from utils.suport.exception import DirectoryNotExist


def write_case_info(item):
    """动态收集用例信息"""

    yaml_path = item.module.__file__.replace('.py', '.yaml')

    # 获取用例ID
    case_name, case_id, _ = re.split("\[|]", item.name)

    # 获取用例所属服务
    env = re.findall("/tests/(.+?)/", yaml_path)[0]

    # 获取用例信息
    case_info = getattr(item.config, env + "_info").get(case_name, {}).get(case_id, {})

    if case_info:
        # 开始写入用例信息
        dynamic.feature(env)
        dynamic.issue(case_info.get("author", "NA"))
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


def write_report_info(session):
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

            # 写入测试环境信息
            env = session.config.getoption('env')
            with open(os.path.join(allure_report_path, 'environment.properties'), 'w+', encoding='utf-8') as f:
                f.write(f"{env}={HOSTS.get(env)}\n")
        except Exception as e:
            logger.warning(f'导入用例分类信息失败！error: {e}')
    else:
        logger.warning(f'导入用例分类信息失败！error: {DirectoryNotExist}')


def collect_logs():
    """
    收集分布式执行时各个worker的日志到master
    :return: None
    """
    # 日志根目录
    log_path = os.path.join(BASE_DIR, 'logs')
    all_logs = os.path.join(BASE_DIR, 'logs', 'all_logs.log')

    for tup in os.walk(log_path, topdown=False):
        with open(all_logs, 'ab') as target:
            for file_name in tup[2]:
                file_path = os.path.join(tup[0], file_name)
                with open(file_path, 'rb+') as origin:
                    for content in origin:
                        target.write(content)
                # seek() 方法用于移动文件读取指针到指定位置。
                # 第一个参数，表示偏移的字节数
                # 第二个参数，表示从哪里开始偏移。默认值是0。0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。
                # target.seek(0, 1)
                # truncate() 方法用于截断文件，如果指定了可选参数 size，则表示截断文件为 size 个字符。
                # 如果没有指定 size，则从当前位置起截断；截断之后 size 后面的所有字符被删除。
                # target.truncate()


def test_results(session, exitstatus):
    """
    统计测试结果
    :param session: pytest session 对象
    :param exitstatus:  执行结束的状态码
    :return:
    """
    # 获取统计报告
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')

    # 用例总数
    total = session.testscollected if session.testscollected else 1

    # 测试耗时
    duration = datetime.now() - session.config.getoption('start_time')

    passed = len(reporter.stats.get('passed', []))
    failed = len(reporter.stats.get('failed', []))
    error = len(reporter.stats.get('error', []))
    skipped = len(reporter.stats.get('skipped', []))
    passrate = '%.2f' % (round(((passed + skipped) / total) * 100)) + '%'
    build_number = session.config.getoption('build_number')
    job_name = session.config.getoption('job_name')
    if exitstatus == 0:
        result = "通过"
    elif exitstatus == 1 or exitstatus == 3:
        result = "失败"
    elif exitstatus == 2:
        result = "中断"
    elif exitstatus == 4:
        result = "错误"
    elif exitstatus == 5:
        result = "无可用的用例"
    else:
        result = "未知"
    return job_name, build_number, total, result, passrate, duration.seconds, passed, failed, skipped, error
