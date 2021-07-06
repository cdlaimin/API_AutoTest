import logging
import os

from loguru import logger

from conf.settings import BASE_DIR


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

def logpath():
    log_path = os.path.join(BASE_DIR, 'logs')
    logfile_path = os.path.join(log_path, '{}.log'.format('test_log'))
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        if not os.path.exists(logfile_path):
            with open(logfile_path, 'w', encoding="utf-8") as fp:
                pass

    return logfile_path


# 重写emit使日志信息可以输出到allure
class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


config = {
    "handlers": [
        {"sink": logpath(), "format": "{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}", "level": "INFO",
         "retention": "1 days", "colorize": True, "enqueue": True},
        {"sink": PropogateHandler(), "format": "{time:YYYY-MM-DD HH:mm:ss}-{message}", "level": "INFO",
         "colorize": False, "enqueue": True}
    ],
    "extra": {"user": "someone"},
}

logger.configure(**config)
