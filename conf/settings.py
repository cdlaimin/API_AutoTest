import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 弃用或失效的用例
DISABLE_ITEMS = [
    # 'test_query_province_002',
]


if __name__ == '__main__':
    print(BASE_DIR)
