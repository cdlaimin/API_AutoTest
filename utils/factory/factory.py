from abc import ABCMeta, abstractmethod


class ClearDB(metaclass=ABCMeta):
    """
    数据库测试数据清理基类
    """

    def __init__(self, database, env):
        self.instance = database(env)

    @abstractmethod
    def clear(self) -> None:
        pass
