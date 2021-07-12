
import pytest


def test_modify_userFace(flow):
    for func in flow:
        func()


if __name__ == '__main__':
    pytest.main(['-s'])
