import pytest

from libs.request import Requests
from utils.onTest.verify_response import verification


def test_query_city(params):
    expect = params.pop('expect')
    response = Requests(**params).requests()

    # 验证结果
    verification(expect, response)


if __name__ == '__main__':
    pytest.main(['-s'])
