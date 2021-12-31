"""
框架使用到的模板
"""

STANDARD_RUN = '''def run({self}, {role}, {api_list}):
    for api in {api_list}:
        # 向报告中添加二级分类信息
        allure.dynamic.story({self}.__doc__ or {self}.__class__.__name__)

        # 向报告中添加测试步骤信息
        with allure.step(api[0]):
            # 先关联数据
            api_name, api_data = relate(api, {self})

            expect = api_data.pop('expect')
            response = call_api({role}, api_data)

            # 验证结果
            verify(expect, response)

            # 保存响应json
            self.__setattr__(api_name, response.json())'''
