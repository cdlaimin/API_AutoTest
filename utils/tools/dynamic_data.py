from faker import Faker


class DynamicData:
    """
    按需添加需要生成的动态数据
    """
    faker = Faker(locale='zh_CN')

    @classmethod
    def mobile(cls):
        return cls.faker.phone_number()


if __name__ == '__main__':
    print(DynamicData.mobile())
