import os
import sys

from utils.common.file_action import read_ini_file

# 项目根路径
BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 应用配置信息
APP_CONFIG = read_ini_file('application.ini')

# 数据库配置
DB_CONFIG = read_ini_file('database.ini')

# 测试结果通知配置
NOTIFICATION_CONFIG = read_ini_file('notification.ini')

# 弃用或失效的用例
DISABLE_ITEMS = [
    # 'test_query_province_002',
]


if __name__ == '__main__':
    print(BASE_URL)
