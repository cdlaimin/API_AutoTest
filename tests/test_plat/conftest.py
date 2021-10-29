import allure
import pytest

from libs.common.login import TestPlat
from libs.database.test_plat import Operation
from utils.test.assemble import build_test_flow, build_test_data


@pytest.fixture()
@allure.step('准备测试数据')
def tp_data(request):
    """
    通用用例入参夹具
    :param request:
    :return:
    """
    # 构造测试数据
    data = build_test_data(request, 'test_plat')

    return data


@pytest.fixture()
@allure.step('准备测试数据')
def tp_flow(request):
    """
    多接口流程用例入参夹具
    :param request:
    :return:
    """
    # 构造测试数据
    func_list = build_test_flow(request, 'test_plat')

    return func_list


@pytest.fixture(scope='session')
def tp_test_session():
    return TestPlat('test').get_session


def pytest_unconfigure(config):
    """
    实例化一次数据库
    清理自动化测试数据
    """
    # 处理自动化测试数据
    db = Operation()
    db.delete_case_by_id()
