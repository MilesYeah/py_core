import random
import string

def choice_data(data):
    """
    获取随机整型数据
    :param data: 数组
    :return:
    """
    _list = data.split(",")
    num = random.choice(_list)
    return num


def random_float(data):
    """
    获取随机整型数据
    :param data: 数组
    :return:
    """
    try:
        start_num, end_num, accuracy = data.split(",")
        start_num = int(start_num)
        end_num = int(end_num)
        accuracy = int(accuracy)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数或精度有误！\n小数范围精度 %s" % data)

    if start_num <= end_num:
        num = random.uniform(start_num, end_num)
    else:
        num = random.uniform(end_num, start_num)
    num = round(num, accuracy)
    return num


def random_int(scope, sep=','):
    """
    获取随机整型数据
    :param sep: scope的分隔符
    :param scope: 数据范围, 用分隔符隔开
    :return:
    """
    try:
        start_num, end_num = scope.split(sep)
        start_num = int(start_num)
        end_num = int(end_num)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数有误！\n %s" % str(scope))
    if start_num <= end_num:
        num = random.randint(start_num, end_num)
    else:
        num = random.randint(end_num, start_num)

    return num


def random_string(num_len):
    """
    从a-zA-Z0-9生成制定数量的随机字符
    :param num_len: 字符串长度
    :return:
    """
    try:
        num_len = int(num_len)
    except ValueError:
        raise Exception("从a-zA-Z0-9生成指定数量的随机字符失败！长度参数有误  %s" % num_len)
    strings = ''.join(random.sample(string.hexdigits, +num_len))
    return strings

