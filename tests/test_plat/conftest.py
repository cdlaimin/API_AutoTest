import allure
import pytest

from libs.login import TestPlat
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
