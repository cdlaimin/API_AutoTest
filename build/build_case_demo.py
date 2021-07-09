from build.case import build_case

path = 'tests/ts/interaction/test_share_trends'
app = 'ts'
api = 'thinksns/index.php?app=public&mod=Feed&act=shareFeed'
method = 'post'
headers = {
    "Referer": "http://{ip}/thinksns/index.php?app=public",
    "Content-Type": "application/x-www-form-urlencoded"
}
fixtures = ['params', ]
data = [
    {
        "body": "$$sentence",
        "type": "feed",
        "app_name": "public",
        "sid": "@@feed_id",
        "comment": 1,
        "curid": "@@feed_id",
        "curtable": "feed"
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
        'case_name': '转发动态',
        'description': '在朋友圈转发一条动态。预期成功。',
        'level': 'M'
    },
]

if __name__ == '__main__':
    build_case(path, app, api, method, headers, data, expect, info_list, fixture=fixtures)
