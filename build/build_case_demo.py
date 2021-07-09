from build.case import build_case

path = 'tests/ts/interaction/test_publish_trends'
app = 'ts'
api = 'thinksns/index.php?app=public&mod=Feed&act=PostFeed'
method = 'post'
headers = {
    "Referer": "http://{ip}/index.php?app=public&mod=Index&act=index",
    "Content-Type": "application/x-www-form-urlencoded"}
fixtures = ['params', ]
data = [
    {
        "body": "$$sentence",
        "type": "post",
        "app_name": "public"
    },
]
expect = [
    {
        "status": 1,
    },
]
info_list = [
    {
        'model': 'ThinkSNS',
        'func': '朋友圈',
        'case_name': '发布动态',
        'description': '在朋友圈发布一条动态。预期成功。',
        'level': 'M'
    },
]

if __name__ == '__main__':
    build_case(path, app, api, method, headers, data, expect, info_list, fixture=fixtures)
