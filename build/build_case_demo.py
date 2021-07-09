from build.case import build_case

path = 'tests/ts/interaction/test_comment_trends'
app = 'ts'
api = 'thinksns/index.php?app=widget&mod=Comment&act=addcomment'
method = 'post'
headers = {
    "Referer": "http://{ip}/thinksns/index.php?app=public",
    "Content-Type": "application/x-www-form-urlencoded"}
fixtures = ['params', ]
data = [
    {
        "app_name": "public",
        "table_name": "feed",
        "row_id": "@@feed_id",
        "app_row_table": "feed",
        "content": "$$sentence",
        "app_detail_url": "http://{ip}/thinksns/index.php?app=public"
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
        'case_name': '评论动态',
        'description': '在朋友圈随机选择一条动态，评论任意内容。预期成功。',
        'level': 'M'
    },
]

if __name__ == '__main__':
    build_case(path, app, api, method, headers, data, expect, info_list, fixture=fixtures)
