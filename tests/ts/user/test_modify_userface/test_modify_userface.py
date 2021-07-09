import pytest

from flow.ts.user.modify_userface import ModifyUserface
from utils.tools.request import Requests
from utils.test.verify import verification


def test_modify_userface(params):
    test = ModifyUserface(params, Requests, verification)

    test.upload_image()
    test.submit()


if __name__ == '__main__':
    pytest.main(['-s'])