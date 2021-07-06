import pytest

from utils.tools.request import Requests
from utils.test.verify import verification


def test_case_name(fixtures):
    expect = fixture.pop('expect')
    response = Requests(**fixture).requests()

    # 验证结果
    verification(expect, response)


if __name__ == '__main__':
    pytest.main(['-s'])
