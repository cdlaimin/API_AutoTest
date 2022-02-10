from pymongo import MongoClient
from bson.objectid import ObjectId

import pytest

from conf import DATABASE
from utils.suport.role import TestPlatRole


def pytest_configure(config):
    # 完成对测试角色对象的初始化
    env = config.getoption("env")
    config.TP_ROLE = TestPlatRole(env)

    # 从mongodb加载测试数据到配置
    configure = DATABASE.get(env + '_mongo')

    con = MongoClient(configure.get("host"), configure.get("port"))
    db = getattr(con, configure.get("db"))
    data_set = getattr(db, configure.get("set"))
    config.tp_data = data_set.find_one({'_id': ObjectId(configure.get("data_id"))})
    config.tp_info = data_set.find_one({'_id': ObjectId(configure.get("info_id"))})


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
