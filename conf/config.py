import os

from conf.settings import BASE_DIR
from utils.action.document import read_ini_file, read_yaml_file

# 应用配置信息
APP_CONFIG = read_ini_file('application.ini')

# 数据库配置
DB_CONFIG = read_ini_file('database.ini')

# 测试结果通知配置
NOTIFICATION_CONFIG = read_ini_file('notification.ini')

# 已经上传到测试平台的用例
UPLOADED_CASES = read_yaml_file(os.path.join(BASE_DIR, 'conf', 'uploaded_case.yaml'))


if __name__ == '__main__':
    print(UPLOADED_CASES)
