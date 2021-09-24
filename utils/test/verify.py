import json
import re


def verify(expect, real: object):
    """
    验证用例执行结果
    :param expect: 预期结果
    :param real: 实际结果，接口响应对象
    :return:
    """

    # 判断是否有需要验证的预期结果，没有则仅完成状态码的校验
    if expect:
        response = real.json()

        # 其次验证实际结果是否与预期一致
        if isinstance(expect, dict):
            if expect.get('status_code'):
                code = expect.pop('status_code')
                assert code == real.status_code, f'预期状态码：{code} 和实际状态码：{real.status_code}不匹配'
            else:
                assert real.status_code in (200, 201), f'预期状态码：(200, 201) 和实际状态码：{real.status_code}不匹配'

            dict_verify(expect, response)
        elif isinstance(expect, list):
            for sub_expect in expect:
                assert sub_expect in response, f'预期值：{sub_expect} 不在响应文本中：{response}'
        else:
            assert expect == response, f'预期值：{expect} 和实际值：{response} 不匹配'
    else:
        assert real.status_code in (200, 201), f'预期状态码：(200, 201) 和实际状态码：{real.status_code}不匹配'


def dict_verify(expect, response):
    """
    相应结果为字典时的通用校验方法
    :param expect: 预期结果的字典
    :param response: 实际相应结果字典
    :return:
    """
    # 其次验证实际结果是否与预期一致
    for key, value in expect.items():
        # 如果预期值是str或者int那么就直接对比
        if isinstance(value, (str, int)):
            # 直接对比之前先判断一下是否是
            if key == 'type':
                assert type(response).__name__ == value, f'类型校验：预期值：{type(response).__name__} 和实际值：{value} 不匹配'
            elif key == 'length':
                assert len(response) == value, f'长度校验：预期值：{len(response)} 和实际值：{value} 不匹配'
            else:
                # 在不是类型和长度校验时，则默认实际结果是字典
                assert value == response.get(key), f'预期值：{expect} 和实际值：{response} 不匹配'

        # 如果预期值是list则便利预期列表中的item是否都在实际结果中能找到
        if isinstance(value, list):
            real_value = response.get(key)
            for sub_value in value:
                assert sub_value in real_value, f'预期值：{sub_value} 不在响应文本中：{real_value}'

        # 如果预期值是dict则再次调用本方法进行递归验证
        if isinstance(value, dict):
            dict_verify(value, response.get(key))


def relate(origin: dict, new: dict):
    """
    origin中，value格式为<xxx>的字符串，则认为需要在new中找到键为xxx的值，替换origin中的value
    """
    # 拆解new字典，将其多级结构拆成单级的字典
    simple_dict = dict()

    def parse_dict(data: dict):
        for key, value in data.items():
            if isinstance(value, (str, int)):
                simple_dict[key] = value
            if isinstance(value, dict):
                parse_dict(value)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        parse_dict(item)

    parse_dict(new)

    # 替换源字典中需要替换的值
    def replace(data: dict):
        data = json.dumps(data)
        sets = set(re.findall(r'<(\w+)>', data))

        for field in sets:
            value = simple_dict.get(field, None)
            # 替换数据
            if isinstance(value, str):
                data = re.sub(fr'<{field}>', value, data)
            if isinstance(value, int):
                data = re.sub(fr'\"<{field}>\"', str(value), data)

        return json.loads(data)

    return replace(origin)
