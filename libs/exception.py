class LoginFailException(BaseException):
    def __init__(self):
        err = '登陆失败，请检查用户名密码、网络等是否正常。'
        BaseException.__init__(self, err)


class DbConfigNotExist(BaseException):
    def __init__(self):
        err = '数据库配置信息不存在。'
        BaseException.__init__(self, err)


class DirectoryPathNotExist(BaseException):
    def __init__(self):
        err = '目标目录不存在。'
        BaseException.__init__(self, err)