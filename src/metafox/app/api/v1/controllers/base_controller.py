from metafox.redis.redis_client import RedisClient

class BaseController:
    
    def __init__(self) -> None:
        self.redis_client = RedisClient()