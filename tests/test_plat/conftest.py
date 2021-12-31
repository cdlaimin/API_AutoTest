from importlib import import_module

import pytest

from utils.suport.role import TestPlatRole


def pytest_configure(config):
    # 完成对测试角色对象的初始化
    env = config.getoption("env")
    config.TP_ROLE = TestPlatRole(env)

    # 加载测试数据到配置
    # 从 libs.data 中读取接口基础数据信息
    data_module = import_module("libs.data")
    config.test_plat = getattr(data_module, "test_plat")


@pytest.fixture(scope='session')
def staff(request):
    """
    普通职员
    """
    return request.config.TP_ROLE.staff


@pytest.fixture(scope="session")
def admin(request):
    """
    管理员
    """
    return request.config.TP_ROLE.admin


