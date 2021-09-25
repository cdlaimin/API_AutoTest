import allure
import pytest

from utils.test.assemble import build_test_params, build_test_flow


@pytest.fixture()
@allure.step('准备测试数据')
def params(request):
    """
    通用用例入参夹具
    :param request:
    :return:
    """
    # 构造测试数据
    data = build_test_params(request)

    return data


@pytest.fixture()
@allure.step('准备测试数据')
def flow(request):
    """
    多接口流程用例入参夹具
    :param request:
    :return:
    """
    # 构造测试数据
    func_list = build_test_flow(request)

    return func_list


@pytest.fixture(scope='session')
def tp_session():
    pass
