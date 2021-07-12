import pytest


def test_create_microBar(flow):
    for func in flow:
        func()


if __name__ == '__main__':
    pytest.main(['-s'])

