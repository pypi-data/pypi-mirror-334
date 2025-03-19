import redis


class RedisClient(object):
    def __init__(self, host, port, db, password, key_prefix=""):
        """
        初始化 Redis 连接
        :param host: Redis 主机地址
        :param port: Redis 端口号
        :param db: Redis 数据库编号
        :param password: Redis 密码（如果有）
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.key_prefix = key_prefix

        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)

    def change_db(self, db):
        try:
            self.redis_client.close()
        except Exception as e:
            pass
        self.redis_client = redis.StrictRedis(host=self.host, port=self.port, db=db,
                                              password=self.password, decode_responses=True)
        return self

    def ping(self):
        """
        检查 Redis 连接是否正常
        :return: Redis 是否正常连接（True 或 False）
        """
        return self.redis_client.ping()

    def set(self, key, value, expire=None, use_prefix=True):
        """
        设置 Redis 键值对
        :param use_prefix:
        :param key: Redis 键
        :param value: 要存储的值（可以是任意 Python 对象）
        :param expire: 过期时间（秒），可选
        """
        key = self.key_prefix + key if use_prefix else key
        if expire:
            self.redis_client.setex(key, expire, value)
        else:
            self.redis_client.set(key, value)

    def get(self, key, use_prefix=True):
        """
        获取 Redis 键对应的值
        :param use_prefix:
        :param key: Redis 键
        :return: 解析后的 Python 对象，如果键不存在则返回 None
        """
        key = self.key_prefix + key if use_prefix else key
        value = self.redis_client.get(key)
        if value is None:
            return None

        return value

    def delete(self, key, use_prefix=True):
        """
        删除 Redis 键
        :param use_prefix:
        :param key: Redis 键
        :return: 删除操作的结果（True 或 False）
        """
        key = self.key_prefix + key if use_prefix else key
        return self.redis_client.delete(key)

    def close(self):
        """
        手动关闭 Redis 连接
        """
        self.redis_client.close()

