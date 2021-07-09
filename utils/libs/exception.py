class LoginFailException(BaseException):
    def __init__(self, err='登陆失败，请检查用户名密码、网络等是否正常。'):
        BaseException.__init__(self, err)


class DbConfigNotExist(BaseException):
    def __init__(self, err='数据库配置信息错误。'):
        BaseException.__init__(self, err)


class DirectoryPathNotExist(BaseException):
    def __init__(self, err='目标目录不存在。'):
        BaseException.__init__(self, err)


class ParamsCheckFailed(BaseException):
    def __init__(self, err='入参校验失败。'):
        BaseException.__init__(self, err)


class RequestMethodInvalid(BaseException):
    def __init__(self, err='请求类型不合法。'):
        BaseException.__init__(self, err)


class ParamsTypeError(BaseException):
    def __init__(self, err='入参类型不合法。'):
        BaseException.__init__(self, err)


class APIRequestError(BaseException):
    def __init__(self, err='接口未知错误。'):
        BaseException.__init__(self, err)
