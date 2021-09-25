import logging
import os
import sys

from loguru import logger

from conf import BASE_DIR


def log_path():
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
        {"sink": log_path, "format": "{time:YYYY-MM-DD HH:mm:ss} {level} {message}", "level": "INFO",
         "encoding": "utf-8", "colorize": False, "enqueue": True},
        # loguru报告重定logging输出
        {"sink": PropagateHandler(), "format": "{time:YYYY-MM-DD HH:mm:ss} {message}", "level": "INFO",
         "colorize": False, "enqueue": True},
        # 输出到控制台
        {"sink": sys.stderr, "format": "{time:YYYY-MM-DD HH:mm:ss} {level} {message}", "level": "INFO",
         "colorize": False, "enqueue": True},
    ],
    "extra": {"user": "someone"}
}

logger.configure(**config)
