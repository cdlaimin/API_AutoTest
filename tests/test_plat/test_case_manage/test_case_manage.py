from utils.test.execute import run


# 用例的 __doc__ 将作为 story 添加到报告中。如果没有 __doc__ 信息则使用 类名。
class TestCaseManage:
    """用例管理"""

    @run
    def test_create_case(self, staff, api_list):
        pass

    @run
    def test_modify_case(self, staff, api_list):
        pass

    @run
    def test_delete_case(self, staff, api_list):
        pass
