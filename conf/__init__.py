import os

from utils.operation.file import load_ini, load_yaml

# 项目根路径
BASE_DIR = os.path.abspath(__file__).rsplit('/', 2)[0]

# 应用配置信息
HOST = load_yaml(os.path.join(BASE_DIR, 'conf', 'hosts.yaml'))

# 数据库配置
DB_CONF = load_yaml(os.path.join(BASE_DIR, 'conf', 'database.yaml'))

# 测试结果通知模版
NOTICE_TEMP = load_ini(os.path.join(BASE_DIR, 'conf', 'notice_temp.ini'))

# 登陆账户信息
ACCOUNT = load_yaml(os.path.join(BASE_DIR, 'conf', 'account.yaml'))
