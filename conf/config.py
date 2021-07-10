from utils.action.document import read_ini_file

# 应用配置信息
APP_CONFIG = read_ini_file('application.ini')

# 数据库配置
DB_CONFIG = read_ini_file('database.ini')

# 测试结果通知配置
NOTIFICATION_CONFIG = read_ini_file('notification.ini')