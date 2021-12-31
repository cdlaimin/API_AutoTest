from requests import Response


def verify(expect: dict, response: Response):
    """
    验证用例执行结果
    :param expect: 预期结果
    :param response: 实际结果，接口响应对象
    :return:
    """

    # 判断 response 类型
    if not isinstance(response, Response):
        assert False, "入参 response 类型错误,期望对象类型 requests.Response "

    # 判断 expect 类型
    if not isinstance(expect, dict):
        assert False, "入参 expect 类型错误,期望对象类型 dict "

    # 如果预期是一个空字典，只判断响应的状态码
    if len(expect) == 0:
        assert response.status_code in (200, 201), f'实际状态码 {response.status_code} 和 预期状态码 (200, 201) 不一致'

    # 验证预期结果
    if len(expect) > 0:
        real_code = response.status_code
        response = response.json()

        # 非正向流程时，状态码往往不是(200, 201)。如果要校验非默认状态码，在 expect 中田间 'status_code' 字段即可
        if expect.get('status_code'):
            code = expect.pop('status_code')
            assert code == real_code, f'实际状态码 {real_code} 和 预期状态码 {code} 不一致'
        else:
            assert real_code in (200, 201), f'实际状态码 {real_code} 和 预期状态码 (200, 201) 不一致'

        # 其他预期项验证
        __verify(expect, response)


def __verify(expect: dict, response: dict):
    """
    校验 expect 中所有 key 的值，是否都与 response 中对应 key 的值相等
    :param expect: 预期结果的字典
    :param response: 实际响应结果字典
    :return:
    """
    # 其次验证实际结果是否与预期一致
    for key, value in expect.items():
        # 如果预期值是str或者int那么就直接对比
        if isinstance(value, (str, int)):
            # 这里支持对 response 进行长度检查，这里的 response 一定是字典
            if key == 'length':
                assert len(response) == value, f'实际长度 {value} 和 预期长度 {len(response)} 不一致'
            else:
                # 在不是类型和长度校验时，则默认实际结果是字典
                assert value == response.get(key), f'KEY:{key} 实际返回值 {response.get(key)} 和 预期值 {value} 不一致'

        # 如果预期值是list则便利预期列表中的item是否都在实际结果中能找到
        if isinstance(value, list):
            real_value = response.get(key)

            # 如果预期列表长度为0，那么要求实际列表长度也为0。非 0 时，不做长度校验
            if len(value) == 0 and len(real_value) != 0:
                assert False, f'KEY:{key} 实际返回列表长度为 {len(real_value)} 与预期列表长度 0 不一致'

            for index, sub_value in enumerate(value):
                # 此处不考虑列表项仍然是列表的情况，此种情况也不能出现在脚本中
                if isinstance(sub_value, (str, int)):
                    assert sub_value in real_value, f'KEY:{key} 实际返回列表 {real_value} 中未找到预期列表项 {sub_value}'
                # 如果列表项是字典，那么要求需要校验的列表项要和实际响应列表项按索引对应
                if isinstance(sub_value, dict):
                    # 判断返回值列表该索引处是否也为字典，如果是则 递归调用 本方法
                    if isinstance(real_value[index], dict):
                        __verify(sub_value, real_value[index])
                        continue
                    assert False, f'KEY:{key} 实际返回列表在索引 {index} 处的列表项与预期类型 dict 不一致'

        # 如果预期值是dict则再次调用本方法进行递归验证
        if isinstance(value, dict):
            if isinstance(response.get(key), dict):
                __verify(value, response.get(key))
            else:
                assert False, f'KEY:{key} 实际返回值的类型与预期类型 dict 不一致'

