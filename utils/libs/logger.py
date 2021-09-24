import logging
import os
import sys

from loguru import logger

from conf import BASE_DIR


# config = {
#     'version': 1,
#     'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
#     'formatters': {
#         'simple': {
#             'format': '%(asctime)s - %(levelname)s - %(message)s',
#         },
#         # 其他的 formatter
#     },
#     'handlers': {
#         'console': {  # 向终端中输出日志
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',  # 打印到控制台的输出类
#             'formatter': 'simple'
#         },
#         'file': {  # 向文件中输出日志
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, "logs", "test_log.log"),  # 日志文件的位置
#             'formatter': 'simple'
#         },
#         # 其他的 handler
#     },
#     'loggers': {
#         # 'StreamLogger': {
#         #     'handlers': ['console'],
#         #     'level': 'DEBUG',
#         #     'propagate': True,  # 是否继续传递日志信息
#         # },
#         'FileLogger': {
#             # 既有 console Handler，还有 file Handler
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         # 其他的 Logger
#     }
# }
#
# #  载入配置
# logging.config.dictConfig(config)
# # StreamLogger = logging.getLogger("StreamLogger")
# # 实例化日志对象
# logger = logging.getLogger("FileLogger")

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
        {"sink": sys.stderr, "format": "{time:YYYY-MM-DD HH:mm:ss} {level} {message}","level": "INFO",
         "colorize": False, "enqueue": True},
    ],
    "extra": {"user": "someone"}
}

logger.configure(**config)
