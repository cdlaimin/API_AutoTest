"""
各个服务的测试数据
"""
import os

from conf import BASE_DIR, load_yaml

test_plat = load_yaml(os.path.join(BASE_DIR, 'libs', 'data', 'test_plat.yaml'))
