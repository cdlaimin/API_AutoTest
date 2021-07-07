from build.case import build_case

path = 'tests/ts/user/test_modify_userface'
app = 'ts'
api = 'thinksns'
method = 'post'
headers = {
    "Referer": "http://{ip}:{port}/thinksns/index.php?app=public&mod=Account&act=avatar",
}
fixtures = ['flow', ]
data = [
    {

    },
]
expect = [
    {
        "status": 1,
    },
]
info_list = [
    {
        'model': '用户',
        'func': '个人中心',
        'case_name': '修改用户头像',
        'description': '修改用户头像：1、上传头像；2、保存修改。 预期成功',
        'level': 'M'
    },
]

if __name__ == '__main__':
    build_case(path, app, api, method, headers, data, expect, info_list, fixture=fixtures)
