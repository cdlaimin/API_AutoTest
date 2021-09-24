class LoginError(BaseException):
    def __init__(self, err='登陆异常，请检查用户名密码、网络等是否正常'):
        BaseException.__init__(self, err)


class ConfNotExist(BaseException):
    def __init__(self, err='期望配置信息不存在'):
        BaseException.__init__(self, err)


class DirectoryNotExist(BaseException):
    def __init__(self, err='目录不存在'):
        BaseException.__init__(self, err)


class RequestError(BaseException):
    def __init__(self, err='异常请求'):
        BaseException.__init__(self, err)
