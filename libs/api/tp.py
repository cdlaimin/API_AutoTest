"""
说明：如果API接口 "Content-Type" 不是 "application/json;charset=UTF-8"，请在接口信息中显示指定headers属性
"""
# 创建用例
create_case = {"route": "/api/case/", "method": "post"}

# 修改用例
modify_case = {"route": "/api/case/", "method": "put"}

# 删除用例
delete_case = {"route": "/api/case/", "method": "delete"}

# 创建任务
create_job = {"route": "/api/testJob/", "method": "post"}

# 指派任务
dispatch_job = {"route": "/api/dispatchJob/", "method": "put"}

# 任务列表
job_list = {"route": "/api/jobList/", "method": "get"}
