import inspect
import json
import types

from utils.suport.exception import FuncBuildError
from utils.suport.logger import api_logger
from utils.suport.templates import STANDARD_RUN
from utils.test import verify, relate


@api_logger
def call_api(client, data: dict):
    """
    负责完成API接口请求工作
    """
    if data.get("data") and 'json' in data['headers']['Content-Type']:
        data['data'] = json.dumps(data['data'])
    if data.get("params") and 'json' in data['headers']['Content-Type']:
        # params 参数中如果还有二级对象，需要将其转成 json 串
        for key, value in data.pop("params").items():
            if isinstance(value, dict):
                value = json.dumps(value)
            data.setdefault("params", {})[key] = value

    return client.request(**data)


def run(func):
    """
    装饰器
    动态生成测试函数
    负责用例的执行
    """
    args = inspect.getfullargspec(func).args
    function = None

    # 根据入参动态选取模板生成code
    if len(args) == 3:
        self, role, api_list = args
        string = STANDARD_RUN.format(self=self, role=role, api_list=api_list)

        # 将code串编译成code对象
        code = compile(source=string, filename=func.__name__, mode="exec").co_consts[0]
        # 创建函数
        # globals 选项为函数提供全局变量。比如函数内部需要调用其他方法，如果不指定会ERROR
        # locals()\globals() 内置函数分别返回局部(所在局部块，这里就是函数内部作用域)/全局(当前模块)的作用域字典
        function = types.FunctionType(code=code, globals=globals(), name=func.__name__)

    # 校验函数
    if not function:
        raise FuncBuildError

    return function
