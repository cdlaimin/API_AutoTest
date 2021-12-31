import json
import re


def __simple_dict(base: dict, simple_dict: dict):
    # 列表项是否全是 str 或 int。
    flag = True

    for key, value in base.items():
        if isinstance(value, (str, int)):
            simple_dict.setdefault(key, []).append(value)
        if isinstance(value, dict):
            __simple_dict(value, simple_dict)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, list):
                    flag = False
                if isinstance(item, dict):
                    flag = False
                    __simple_dict(item, simple_dict)
            # 如果列表项中只有str和int，就把整个列表作为值保存
            if flag:
                simple_dict.setdefault(key, []).append(value)


def __search(base: dict, key: str, api=None):
    """
    从 base 字典中找出 key 对应的值，并返回
    """
    # 拆解base字典，将其多级结构拆成单级的字典
    simple_dict = dict()

    __simple_dict(base, simple_dict)

    try:
        return simple_dict[key]
    except KeyError:
        raise KeyError(f"API接口 {api} 返回json中未找到键 {key}")


def relate(api: tuple, instance: object):
    """
    为API接口实现数据关联
    """
    api_name, api_value = api

    # 找出需要关联的值
    data = json.dumps(api_value)
    sets = set(re.findall(r'<(\w+\.\w+)>', data))

    for field in sets:
        # 根据关联规则解析出需要关联的接口和字段
        pre_api_name, key = field.split('.', 1)
        try:
            # 从 instance 中获取 api_name 对应接口的返回json
            json_dict = getattr(instance, pre_api_name)
        except AttributeError:
            raise AttributeError(f"实例对象 {instance.__class__.__name__} 中未找属性 {pre_api_name}")

        # 从json_dict中找出key对应的值
        values = __search(json_dict, key, pre_api_name)

        # 当 values 长度为 1 时，表示可直接进行替换
        if len(values) == 1:
            value = values[0]
            if isinstance(value, str):
                data = re.sub(fr'<{field}>', value, data)
            elif isinstance(value, (int, list)):
                data = re.sub(fr'(\"<{field}>\"|\'<{field}>\')', str(value), data)
            else:
                raise TypeError("单值 关联时出现非法数据类型")
        # 长度大于 1 时，表示要要替换多个值
        else:
            if isinstance(values[0], str):
                value = ", ".join(["'" + item + "'" for item in values])
            elif isinstance(values[0], int):
                value = ", ".join(str(item) for item in values)
            else:
                raise TypeError("多值 关联时出现非法数据类型"
                                "此时我们默认 values 中的值类型都是一样的，且只能是 int、str 两种类型"
                                "如果是其他类型，那么就需要优化测试数据")

            data = re.sub(fr'(\"<{field}>\"|\'<{field}>\')', value, data)

    return api_name, json.loads(data)
