import os

from redis import Redis
from dotenv import load_dotenv
from metafox_shared.constants.api_constants import *
from metafox_shared.dal.idatastore import IDataStore

class RedisClient(IDataStore):
    def __init__(self) -> None:
        load_dotenv()
        self.redis = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0),
            decode_responses=True
        )
        
        print("Redis connection established.")
        
    def set(self, key: str, value: str, collection_name: str) -> None:
        if self.redis.exists(key):
            raise Exception(f"Key {key} already exists.")
        
        self.redis.set(key, value)
        
    def get(self, key: str, collection_name: str) -> str:
        if self.redis.exists(key):
            return self.redis.get(key)
        
        raise Exception(f"Key {key} does not exist.")
        
    def update(self, key: str, value: str, collection_name: str) -> None:
        if self.redis.exists(key):
            self.redis.delete(key)
            self.redis.set(key, value)
        else:
            self.redis.set(key, value)
    
    def delete(self, key: str, collection_name: str) -> None:
        if self.redis.exists(key):
            self.redis.delete(key)
            return
        
        raise Exception(f"Key {key} does not exist.")
            
    def get_automl_job_ids(self, collection_name: str) -> list:
        cursor = '0'
        matching_keys = []
        
        while cursor != 0:
            cursor, keys = self.redis.scan(cursor = cursor)
            
            for key in keys:
                if key.startswith(CELERY_KEY_PREFIX):
                    matching_keys.append(key.replace(CELERY_KEY_PREFIX, ""))
                    
        return matching_keys
        
    def get_keys_by_pattern(self, pattern: str, collection_name: str) -> list:
        cursor = '0'
        redis_keys = []

        while cursor != 0:
            cursor, keys = self.redis.scan(cursor=cursor, match=pattern)
            redis_keys.extend(keys)

        return redis_keys

    def close(self) -> None:
        print("Redis client destroyed.")
        self.redis.close()