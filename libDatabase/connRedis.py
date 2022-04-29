import redis

from handlerLogger import logger


class RedisHandler:
    """ redis 缓存读取封装 """

    def __init__(self, host='121.43.35.47', port=6379, db=0, password=123456, charset='UTF-8'):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.charset = charset

    # 实现with方法
    def __enter__(self):
        try:
            self.redis = redis.Redis(self.host, port=self.port, password=self.password, decode_responses=True,
                                     db=self.db)
        except Exception as e:
            logger.error(f'数据库链接超时请检查：{e}')
        return self

    # 自动关闭
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.redis.close()
            self.redis.quit()
        except Exception as e:
            logger.error(f"数据库关闭失败：{e}")

    def set_string(self, name: str, value, ex=None, px=None, nx=False, xx=False) -> None:
        """
        缓存中写入 str（单个）
        :param name: 缓存名称
        :param value: 缓存值
        :param ex: 过期时间（秒）
        :param px: 过期时间（毫秒）
        :param nx: 如果设置为True，则只有name不存在时，当前set操作才执行（新增）
        :param xx: 如果设置为True，则只有name存在时，当前set操作才执行(修改）
        :return:
        """
        self.redis.set(name, value, ex=ex, px=px, nx=nx, xx=xx)

    def key_exit(self, key):
        """
        判断redis中的key是否存在
        :param key:
        :return:
        """

        return self.redis.exists(key)

    def incr(self, key):
        """
        使用 incr 方法，处理并发问题
        当 key 不存在时，则会先初始为 0, 每次调用，则会 +1
        :return:
        """
        self.redis.incr(key)

    def get_key(self, name) -> str:
        """
        读取缓存
        :param name:
        :return:
        """
        return self.redis.get(name)

    def set_many(self, *args, **kwargs):
        """
        批量设置
        支持如下方式批量设置缓存
        eg: set_many({'k1': 'v1', 'k2': 'v2'})
            set_many(k1="v1", k2="v2")
        :return:
        """
        self.redis.mset(*args, **kwargs)

    def get_many(self, *args):
        """获取多个值"""
        results = self.redis.mget(*args)
        return results

    def del_all_cache(self):
        """清理所有现在的数据"""
        for key in self.redis.keys():
            self.del_cache(key)

    def del_cache(self, name):
        """
        删除缓存
        :param name:
        :return:
        """
        self.redis.delete(name)



if __name__ == '__main__':

    pass