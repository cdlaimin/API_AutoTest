"""
框架使用到的模板
"""

STANDARD_RUN = \
    '''def run({self}, {role}, {api_list}):
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

REPORT = \
    '''### {title} [点击查看报告]({url})
    
    #### 测试结果
    状态: {result}
    通过率: **{pass_rate}**
    耗时: **{h}小时 {m}分 {s}秒**
    
    #### 用例统计
    - 总数: {total}
    - 通过: {passed}
    - 失败: {failed}
    - 跳过: {skipped}
    - 错误: {error}'''
