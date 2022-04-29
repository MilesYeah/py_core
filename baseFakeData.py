from faker import Faker


def fakerdata(data):
    """
    :param data: phone_number 手机号: "$faker(phone_number)$" idcard 身份证: "$faker(idcard)$"
    province 随机生成省  city 随机生成市
    :return:
    """
    fake = Faker("zh_CN")
    if data == "idcard":
        value = fake.ssn()
        return value
    elif data == "province":
        value = fake.province()
        return value
    elif data == "city":
        value = fake.city()
        return value
    elif data == "phone_number":
        value = fake.phone_number()
        return value
    elif data == "name":
        value = fake.name()
        return value
    elif data == "email":
        value = fake.email()
        return value

