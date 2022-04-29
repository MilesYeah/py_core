import base64
import hashlib
import uuid as uid


def md5(data, encoding="utf-8"):
    """
    md5加密
    :param encoding: coding for data
    :param data:想要加密的字符
    :return:
    """
    m1 = hashlib.md5()
    m1.update(data.encode(encoding))
    data = m1.hexdigest()
    return data


def uuid():
    '''
    生成 UUID
    :return:
    '''
    return uid.uuid1()


def bs64(data):
    """base64加密处理"""
    bs = base64.b64encode(data.encode('utf-8'))
    return bs


if __name__ == '__main__':

    print()
