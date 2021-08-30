def verification(expect, real: object):
    """
    验证用例执行结果
    :param expect: 预期结果
    :param real: 实际结果，接口响应对象
    :return:
    """
    # 首先判断响应状态码
    try:
        if expect.get('status_code'):
            code = expect.pop('status_code')
            assert code == real.status_code, f'预期状态码：{code} 和实际状态码：{real.status_code}不匹配'
        else:
            assert real.status_code in (200, 201), f'预期状态码：(200, 201) 和实际状态码：{real.status_code}不匹配'
    except AttributeError:
        assert real.status_code in (200, 201), f'预期状态码：(200, 201) 和实际状态码：{real.status_code}不匹配'

    # 判断是否有需要验证的预期结果，没有则仅完成状态码的校验
    if expect:
        response = real.json()
    else:
        return

    # 其次验证实际结果是否与预期一致
    if isinstance(expect, list):
        for sub_expect in expect:
            assert sub_expect in response, f'预期值：{sub_expect} 不在响应文本中：{response}'
    elif type(expect) in (str, int):
        assert expect == response, f'预期值：{expect} 和实际值：{response} 不匹配'
    else:
        dict_verify(expect, response)


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
        if type(value) in (str, int):
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
