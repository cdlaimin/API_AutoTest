import random
import time

from faker import Faker


class FakerData:
    """
    按需添加需要生成的动态数据
    文本替换方式：$$ + 方法名。例如：{"name": "$$user_name"}
    """
    zh_faker = Faker(locale='zh_CN')
    en_faker = Faker()

    @classmethod
    def mobile(cls):
        """随机手机号"""
        return cls.zh_faker.phone_number()

    @classmethod
    def msisdn(cls):
        """随机电话号"""
        return cls.zh_faker.msisdn()

    @classmethod
    def email(cls):
        """随机邮箱"""
        return cls.zh_faker.free_email()

    @classmethod
    def address(cls):
        """随机地址"""
        return cls.zh_faker.address()

    @classmethod
    def nickname(cls):
        """随机人名(中文)"""
        return cls.zh_faker.name()

    @classmethod
    def file_path(cls):
        """随机文件路径"""
        return cls.en_faker.file_path(depth=3, extension='py')

    @classmethod
    def username(cls):
        """随机用户名(英文)"""
        return cls.en_faker.user_name()

    @staticmethod
    def job_type(start: int = 0, end: int = 4):
        """测试任务类型"""
        return random.randint(start, end)

    @staticmethod
    def case_priority(start: int = 1, end: int = 3):
        """用例等级"""
        return random.randint(start, end)

    @classmethod
    def sentence(cls):
        """生成一段中文文字信息"""
        return cls.zh_faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)

    @classmethod
    def thirteen_timestamp(cls):
        """十三位时间戳"""
        return int(time.time() * 1000)

    @classmethod
    def format_time(cls):
        """格式化时间 %Y-%m-%d %H:%M:%S"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cls.thirteen_timestamp() / 1000))


if __name__ == '__main__':
    print(FakerData.file_path())
    print(FakerData.username())
    print(FakerData.nickname())
