import random

from faker import Faker

from utils.action.database import Database


class DynamicData:
    """
    按需添加需要生成的动态数据
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
        """随机人名"""
        return cls.faker.name()

    @classmethod
    def count(cls):
        """生成一个1～10之间的随机数"""
        return random.randint(1, 10)


class StaticData:
    """集中查询修改数据库等静态数据"""

    md_db_conn = Database('meiduo')

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


if __name__ == '__main__':
    print(StaticData.delete_address_id())
