import json

from utils.libs.decorator import api_logger


@api_logger
def start_test(session, data: dict):
    if 'json' in data['headers']['Content-Type'] and data['data']:
        data['data'] = json.dumps(data['data'])
    return session.request(**data)
