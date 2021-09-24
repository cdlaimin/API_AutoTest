import os

from utils.action.document import load_ini, load_yaml

# 项目根路径
BASE_DIR = os.path.abspath(__file__).rsplit('/', 2)[0]

# 应用配置信息
APP_CONFIG = load_yaml(os.path.join(BASE_DIR, 'conf', 'hosts.yaml'))

# 数据库配置
DB_CONFIG = load_ini(os.path.join(BASE_DIR, 'conf', 'database.ini'))

# 测试结果通知配置
NOTIFICATION_CONFIG = load_ini(os.path.join(BASE_DIR, 'conf', 'notification.ini'))

# 已经上传到测试平台的用例
UPLOADED_CASES = load_yaml(os.path.join(BASE_DIR, 'conf', 'uploaded_case.yaml'))


if __name__ == '__main__':
    print(APP_CONFIG)
