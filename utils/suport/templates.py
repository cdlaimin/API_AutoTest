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

REPORT = '''### {title} [点击查看报告]({url})\n\n\

#### 功能模块
> 1、用例管理\n\
> 2、任务管理\n\
\n\
测试结果: **{result}**\n\
通过率: **{pass_rate}**\n\
测试耗时: **{h}小时 {m}分 {s}秒**\n\n\

用例总数:**{total}** \n\n\
- 通过用例: {passed}\n\
- 失败用例: {failed}\n\
- 跳过用例: {skipped}\n\
- 错误用例: {error}'''
