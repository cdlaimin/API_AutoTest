import logging
import os
import sys
import warnings
from functools import wraps

from loguru import logger
from pytest import deprecated_call
from requests.exceptions import BaseHTTPError

from conf import BASE_DIR
from utils.suport.exception import RequestError


def log_path():
    """
    日志文件路径
    """
    path = os.path.join(BASE_DIR, 'logs')
    log_file = os.path.join(path, '{}.log'.format('access_log'))
    if not os.path.exists(path):
        os.makedirs(path)
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding="utf-8") as fp:
                pass

    return log_file


# 重写emit使日志信息可以输出到allure
class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


config = {
    "handlers": [
        # 配置info日志
        {"sink": log_path(), "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", "level": "INFO",
         "colorize": False, "enqueue": True},
        # loguru报告重定logging输出
        {"sink": PropagateHandler(), "format": "| {time:YYYY-MM-DD HH:mm:ss} | {message}", "level": "INFO",
         "colorize": False, "enqueue": True, "backtrace": True, "diagnose": True},
        # 输出到控制台
        {"sink": sys.stdout, "level": "INFO", "colorize": True, "enqueue": False}
    ],
    "extra": {"user": "someone"}
}

logger.configure(**config)


def api_logger(func):
    """
    装饰器
    采集API接口调用时的日志信息
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except BaseHTTPError as e:
            logger.error(f'接口调用异常: {str(e)}')
            raise RequestError
        else:
            logger.info(f'请求地址:{response.request.url}')
            logger.info(f'请求方式:{response.request.method}')
            logger.info(f"请求体:{response.request.body if response.request.body else None}")

            # 根据响应状态码确实使用什么日志方法
            log = getattr(logger, 'info' if response.status_code in (200, 201) else 'error')
            log('状态码:{}'.format(response.status_code))
            try:
                # deprecated_call() 将被标记了 DeprecationWarning 或者 PendingDeprecationWarning 的函数能够正常被调用。
                # 不会在执行时出现 相应的 warning 信息。
                with deprecated_call():
                    # DeprecationWarning 告警不再建议此操作。此处和deprecated_call配合使用，使其无效。
                    # 如果实际需要提示时，去掉deprecated_call()上下文即可
                    warnings.warn('主动抛出警告', DeprecationWarning)
                    log('响应体:{}'.format(response.text.encode('latin-1').decode('unicode_escape')))
            except UnicodeError:
                log('响应体:{}'.format(response.text))
        return response

    return wrapper
