import os
import re
from datetime import datetime

import pytest
import xdist
from loguru import logger

from conf import BASE_DIR
from utils.suport.report import collect_item_info, write_report_information
from utils.operate.document import get_case_id
from utils.suport.gather import gather_logs, gather_results
from utils.suport.notice import send_wechat, send_dingtalk


def pytest_addoption(parser):
    """
    初始化钩子
    注册argparse-style选项以及ini-style配置值，在测试运行开始调用一次。
    parser (_pytest.config.Parser)
        添加命令行选项使用pytest.addoption(…)
        添加ini-file值使 用parser.addini(…)
    之后可以通过config对象来访问：
        config.getoption(name) 来获取命令行选项的值
        config.getini(name) 来获取从ini-style文件中读取的值
    :param parser:
    :return:
    """
    parser.addoption('--target', action='store', type=str, default='all', help='执行哪些agent，默认执行全部')
    parser.addoption('--job_name', action='store', type=str, default=None, help='jenkins执行时，job任务名称')
    parser.addoption('--build_number', action='store', type=int, default=None, help='当前job的构建number')
    parser.addoption('--send_wechat', action='store', type=bool, default=False, help='是否发送测试报告到企微群')
    parser.addoption('--wechat_token', action='store', type=str, default=None, help='企微群消息token')


def pytest_sessionstart(session):
    """
    完成初始化，创建session对象后，调用collection之前的钩子
    :param session: pytest Session 对象
    :return:
    """
    # 分布式执行测试时
    if xdist.is_xdist_master(session):
        # 将测试开始时间记录到option
        session.config.option.start_time = datetime.now()
        # 设置环境变量
        os.environ.setdefault('PYTEST_XDIST_WORKER', 'master')


def pytest_generate_tests(metafunc):
    """
    用例收集阶段钩子
    实现夹具参数化。根据当前测试用例调用的夹具，对夹具进行参数化
    :param metafunc: 帮助实现参数化的钩子默认参数
    :return: None
    """
    yaml_path = metafunc.module.__file__.replace('.py', '.yaml')
    case_name = metafunc.function.__name__
    # fixtures = metafunc.fixturenames
    fixtures = metafunc.definition._fixtureinfo.argnames
    ids = get_case_id(yaml_path, case_name)

    # 夹具参数化
    for fixture in fixtures:
        if fixture in ('tp_data', 'tp_flow'):  # 维护需要参数化的夹具
            metafunc.parametrize(fixture, ids, indirect=True)


def pytest_ignore_collect(path, config):
    """
    忽略收集用例钩子
    根据要测试app来收集用例
    :param path: 当前收集路径的path类
    :param config: pytest config 对象
    :return:
    """
    agent = config.getoption('target')

    # 如是app是默认值all则收集所有用例
    if agent == 'all':
        pass
    # 如果没有当前收集路径不是测试app所在路径，则忽略收集
    # return True 表示忽略当前收集的path
    elif not re.match(os.path.join(BASE_DIR, 'tests', agent), path.__str__()):
        return True


# xdist分布式执行时调用，xdist内部钩子，不是pytest钩子
def pytest_xdist_make_scheduler(config, log):
    """
    用例收集完成后，分发用例时调用的钩子
    自定义用例分发规则
    :param config:
    :return:
    """
    from xdist.scheduler import LoadScopeScheduling

    class MyScheduler(LoadScopeScheduling):
        # 重写用例分发函数
        def _split_scope(self, nodeid):
            # 此处定义具体的分发规则：
            #     pass
            # # 如果不自定义，则调用父类分发方法
            super(MyScheduler, self)._split_scope(nodeid)

    scheduler = MyScheduler(config=config, log=log)
    return scheduler


# 这里的装饰器和yield生成器，对钩子函数进行包装。在yield处，将将钩子函数的执行结果返回给yield
@pytest.hookimpl(hookwrapper=True)  # 也可以用@pytest.mark.hookwrapper 两者作用相同
def pytest_runtest_makereport(item, call):
    """
    执行阶段钩子
    钩子函数被调用时，会创建一个包含setup、call、teardown三个阶段的测试报告
    :param item: 当前测试用例对象
    :param call: 三个执行阶段的信息。三个属性：when(setup、call、teardown)、excinfo、result(一个列表)
    :return:
    """
    # 获取当前接行阶段_Result对象
    out = yield
    if call.excinfo:
        logger.error(f'捕获异常：{call.excinfo}')
    if call.when == 'call':
        # 动态收集用例信息到allure
        collect_item_info(item)

        # 获取当前阶段执行结果的报告对象。三个属性：阶段属性when、阶段执行结果属性outcome、nodeid
        # when取值：setup、call、teardown
        # outcome取值：failed、passed
        # nodeid(测试用例的名字)
        result = out.get_result()
        getattr(logger, 'info' if result.outcome == 'passed' else 'error')(f'测试结果:{result.outcome}')


def pytest_sessionfinish(session, exitstatus):
    """
    测试完成后，session关闭之前的钩子
    :param session: pytest Session 对象
    :param exitstatus: 测试结果状态吗
    :return:
    """
    # 分布式执行时，收集测试执行结果，并发送到测试群
    if xdist.is_xdist_master(session):
        # 为allure报告添加结果分类和环境信息
        write_report_information(session)

        # 发送测试结果到测试群。钉钉或者企业微信
        results = gather_results(session, exitstatus)
        send_wechat(*results, session.config.getoption('wechat_token'))
        # send_dingtalk(*results)


def pytest_unconfigure(config):
    """
    进程退出之前的钩子
    :param config: pytest Config 对象
    :return:
    """
    if os.environ.get('PYTEST_XDIST_WORKER') == 'master':
        # 分布式执行时，收集从机上的日志到master上
        gather_logs()
