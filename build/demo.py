from build.build_case import build_case
from build.upload_case import async_collect, upload_case

path = 'tests/ts/user/test_modify_userFace'
app = 'ts'
fixtures = ['flow', ]
json = [
    {
        "step": {
            "name": "上传图片",
            "setup": ["IMAGE", r"self.step_01['files'] = files"],
            "teardown": [r"self.step_02['data']['picurl'] = response.json()['data']['picurl']"]
        },
        "data": {},
        "url": "http://{ip}:{port}/thinksns/index.php?app=public&mod=Account&act=doSaveAvatar&step=upload",
        "headers": {
            "Referer": "http://{ip}:{port}/thinksns/index.php?app=public&mod=Account&act=avatar"
        },
        "app": "ts",
        "method": "post",
        "expect": {
            "data": {
                "type": "dict",
                "length": 4
            },
            "status": "1"
        }
    },
    {
        "step": {
            "name": "确认提交",
        },
        "data": {},
        "url": "http://{ip}:{port}/thinksns/index.php?app=public&mod=Account&act=doSaveAvatar&step=save",
        "headers": {
            "Referer": "http://{ip}:{port}/thinksns/index.php?app=public&mod=Account&act=avatar"
        },
        "app": "ts",
        "method": "post",
        "expect": {
            "data": {
                "type": "dict",
                "length": 4
            },
            "status": 1
        }
    }
]

yaml = [
    {
        'model': 'ThinkSNS',
        'func': '个人中心',
        'case_name': '修改用户头像',
        'description': '修改用户头像：1、上传头像；2、保存修改。 预期成功',
        'level': 'M'
    },
]

if __name__ == '__main__':
    build_case(path, app, fixtures, json, yaml)

    # async_collect("tests/ts/interaction")
    # upload_case()




