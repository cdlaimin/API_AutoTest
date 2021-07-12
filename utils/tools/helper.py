import time
import warnings
from functools import wraps

from pytest import deprecated_call
from requests.exceptions import HTTPError, SSLError, Timeout, URLRequired, TooManyRedirects

from utils.libs.logger import logger
from utils.libs.exception import APIRequestError


def api_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except (HTTPError, SSLError, Timeout, URLRequired, TooManyRedirects) as e:
            raise APIRequestError(f'请求失败，错误信息:' + str(e))
        else:
            logger.info(f'请求地址:{response.request.url}')
            logger.info(f'请求方式:{response.request.method}')
            logger.info(f'请求头:{response.request.headers}')
            logger.info(f"请求体:{response.request.body[:200] if response.request.body else None}")

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
                    log('响应体:{}'.format(response.text.encode('latin-1').decode('unicode_escape'))[:300])
            except UnicodeError:
                log('响应体:{}'.format(response.text[:300]))
        return response

    return wrapper


def resolve_frequent_operation(func):
    """处理频繁操作问题"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        error_text = '发布内容过于频繁，请稍后再试'
        try:
            # 屏蔽DeprecationWarning告警
            with deprecated_call():
                response_text = response.text.encode('latin-1').decode('unicode_escape')
        except UnicodeError:
            response_text = response.text

        if error_text in response_text:
            time.sleep(5)
            response = func(*args, **kwargs)
        return response

    return wrapper


if __name__ == '__main__':
    aa = getattr(logger, 'info' if 200 in (200, 201, 301, 302, 304) else 'error')
    aa('aaaaa')
