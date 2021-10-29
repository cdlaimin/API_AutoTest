import pytest


@pytest.mark.test_plat
def test_dispatch_job(tp_test_session, tp_flow):
    for func in tp_flow:
        func(tp_test_session)
