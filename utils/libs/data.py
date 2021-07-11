import random

from faker import Faker

from utils.action.database import DataBase


class DynamicData:
    """
    按需添加需要生成的动态数据
    文本替换方式：$$ + 方法名
    """
    faker = Faker(locale='zh_CN')

    @classmethod
    def mobile(cls):
        """随机手机号"""
        return cls.faker.phone_number()

    @classmethod
    def msisdn(cls):
        """随机电话号"""
        return cls.faker.msisdn()

    @classmethod
    def email(cls):
        """随机邮箱"""
        return cls.faker.free_email()

    @classmethod
    def address(cls):
        """随机地址"""
        return cls.faker.address()

    @classmethod
    def people_name(cls):
        """随机人名(中文)"""
        return cls.faker.name()

    @classmethod
    def user_name(cls):
        """随机用户名(英文)"""
        return cls.faker.user_name()

    @classmethod
    def const_password(cls):
        """固定测试密码"""
        return 'Zj123456'

    @classmethod
    def count(cls):
        """生成一个1～10之间的随机数"""
        return random.randint(1, 10)

    @classmethod
    def sentence(cls):
        """生成一段中文文字信息"""
        return cls.faker.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)


class MdData:
    """
    美多数据库
    文本替换方式：$$ + 方法名
    """

    md_db_conn = DataBase('meiduo')

    @classmethod
    def update_address_id(cls):
        """查询一条有效的收货地址id"""
        sql = "select id from tb_address where is_deleted = 0 limit 1;"
        return cls.md_db_conn.query_one(sql)[0]

    @classmethod
    def delete_address_id(cls):
        """查询一条有效的收货地址id"""
        sql = "select id from tb_address where is_deleted = 0 order by create_time desc limit 1;"
        return cls.md_db_conn.query_one(sql)[0]


class TsData:
    """
    ThinkSNS数据库
    文本替换方式：$$ + 方法名
    """
    ts_db_conn = DataBase('ts')

    @classmethod
    def all_user_email(cls) -> list:
        """
        查询所有用户邮箱
        :return: list
        """
        sql = "SELECT email FROM ts_user where uname != '管理员';"
        query_set = cls.ts_db_conn.query_many(sql)
        return list(map(lambda x: x[0], query_set))

    @classmethod
    def user_email(cls):
        """随机获得一个用户邮箱"""
        user_emails = TsData.all_user_email()
        return random.choice(user_emails)

    @classmethod
    def feed_id(cls):
        """返回一个str的feed_id"""
        sql = "SELECT DISTINCT feed_id FROM ts_feed_data;"
        query_set = cls.ts_db_conn.query_many(sql)
        feed_ids = list(map(lambda x: x[0], query_set))
        return random.choice(feed_ids).__str__()


if __name__ == '__main__':
    # print(StaticData.delete_address_id())
    # print(DynamicData.user_name())
    print(TsData.feed_id())
