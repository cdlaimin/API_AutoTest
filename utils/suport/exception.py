class LoginError(BaseException):
    def __init__(self, err='登陆异常，请检查用户名密码、网络等是否正常'):
        BaseException.__init__(self, err)


class ConfNotExist(BaseException):
    def __init__(self, err='配置信息不存在'):
        BaseException.__init__(self, err)


class DirectoryNotExist(BaseException):
    def __init__(self, err='目录不存在'):
        BaseException.__init__(self, err)


class RequestError(BaseException):
    def __init__(self, err='异常请求'):
        BaseException.__init__(self, err)


class CaseStepsError(BaseException):
    def __init__(self, err='用例测试步骤信息错误'):
        BaseException.__init__(self, err)


class SourceDataError(BaseException):
    def __init__(self, err='测试数据源异常'):
        BaseException.__init__(self, err)


class FuncBuildError(BaseException):
    def __init__(self, err='动态构建测试函数失败'):
        BaseException.__init__(self, err)

