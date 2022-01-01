import os

from utils.tools.file import load_ini, load_yaml

# 项目根路径
BASE_DIR = os.path.abspath(__file__).rsplit('/', 2)[0]

# 应用配置信息
HOSTS = load_yaml(os.path.join(BASE_DIR, 'conf', 'hosts.yaml'))

# 数据库配置
DATABASE = load_yaml(os.path.join(BASE_DIR, 'conf', 'database.yaml'))

# 登陆账户信息
ACCOUNT = load_yaml(os.path.join(BASE_DIR, 'conf', 'account.yaml'))
