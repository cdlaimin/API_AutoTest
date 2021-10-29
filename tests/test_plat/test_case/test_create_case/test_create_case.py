import pytest

from utils.test.execute import start_test
from utils.test.verify import verify


@pytest.mark.test_plat
def test_create_case(tp_test_session, tp_data):
    expect = tp_data.pop('expect')
    response = start_test(tp_test_session, tp_data)
    # 验证结果
    verify(expect, response)
