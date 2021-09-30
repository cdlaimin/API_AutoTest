import json
import re

from utils.suport.decorator import api_logger, repeats


@repeats
@api_logger
def start_test(session, data: dict):
    if 'json' in data['headers']['Content-Type'] and data['data']:
        data['data'] = json.dumps(data['data'])
    return session.request(**data)


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
