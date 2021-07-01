def verification(expect: dict, real: object):
    """
    验证用例正向执行结果
    :param expect: 预期结果
    :param real: 实际结果，接口响应对象
    :return:
    """
    # 首先判断响应状态吗
    assert real.status_code == 200 or 201

    # 其次验证实际结果是否与预期一致
    response = real.json()
    for key, value in expect.items():
        # 如果预期值是str或者int那么就直接对比
        if type(value) == str or type(value) == int:
            # 直接对比之前先判断一下是否是
            if key == 'type':
                assert type(response).__name__ == value
            elif key == 'length':
                assert len(response) == value
            else:
                # 在不是类型和长度校验时，则默认实际结果是字典
                assert value == response.get(key)
        # 如果预期值是dict则进入下一级校验
        if type(value) == dict:
            real_value = response.get(key)
            for sub_key, sub_value in value.items():
                # 根据预期字典中的校验类型进行校验
                if sub_key == 'type':
                    assert type(real_value).__name__ == sub_value
                elif sub_key == 'length':
                    assert len(real_value) == sub_value
                # 如果不属于以上两种，则把sub_value当作子串到响应文本中进行对比。存在则校验通过
                else:
                    assert str(sub_value) in str(response)
