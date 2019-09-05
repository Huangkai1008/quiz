import redis


class RedisClient:
    """
    Redis扩展客户端
    """

    def __init__(self):
        self.pool = None  # 连接池
        self.r = None  # redis连接
        self.pipe = None  # redis管道

    def init_app(self, app):
        redis_url = app.config['REDIS_URL']
        self.pool = redis.ConnectionPool.from_url(redis_url, decode_responses=True)  # 创建redis连接池
        self.r = redis.StrictRedis(connection_pool=self.pool)  # 创建Redis连接
        self.pipe = self.r.pipeline(transaction=True)  # 创建连接管道
