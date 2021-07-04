import pytest

from utils.tools.request import Requests
from utils.test.verify import verification


def test_query_cart(params):
    expect = params.pop('expect')
    response = Requests(**params).requests()

    # 验证结果
    verification(expect, response)


if __name__ == '__main__':
    pytest.main(['-s'])
