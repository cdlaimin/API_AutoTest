from libs.logger import logger


def verification(expect, real: object):
    """
    验证用例执行结果
    :param expect: 预期结果
    :param real: 实际结果，接口响应对象
    :return:
    """
    logger.info('响应体:' + real.text)
    response = real.json()

    # 首先判断响应状态吗
    if expect.get('status_code'):
        assert expect.pop('status_code') == real.status_code
    else:
        assert real.status_code in (200, 201)

    # 其次验证实际结果是否与预期一致
    if type(expect) == list:
        for sub_expect in expect:
            assert sub_expect in response
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
                assert type(response).__name__ == value
            elif key == 'length':
                assert len(response) == value
            else:
                # 在不是类型和长度校验时，则默认实际结果是字典
                assert value == response.get(key)

        # 如果预期值是list则便利预期列表中的item是否都在实际结果中能找到
        if type(value) == list:
            real_value = response.get(key)
            for sub_value in value:
                assert sub_value in real_value

        # 如果预期值是dict则再次调用本方法进行递归验证
        if type(value) == dict:
            dict_verify(value, response.get(key))
