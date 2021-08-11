import pytest

from utils.tools.request import Requests
from utils.test.verification import verification


@pytest.mark.MEIDUO
def test_comment_trends(params):
    expect = params.pop('expect')
    response = Requests(**params).requests()

    # 验证结果
    verification(expect, response)


if __name__ == '__main__':
    pytest.main(['-s'])
