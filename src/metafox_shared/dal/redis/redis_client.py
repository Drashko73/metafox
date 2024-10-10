import os
import uuid

from redis import Redis
from datetime import datetime
from dotenv import load_dotenv
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.constants.api_constants import *

class RedisClient (IDataStore):
    def __init__(self) -> None:
        load_dotenv()
        self.redis = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0),
            decode_responses=True,
        )
        
    def set(self, key: str, value: str, ex: int = None) -> None:
        if self.redis.exists(key):
            raise Exception(f"Key {key} already exists.")
        
        self.redis.set(key, value, ex=ex)
        
    def get(self, key: str) -> str:
        if self.redis.exists(key):
            return self.redis.get(key)
        
        raise Exception(f"Key {key} does not exist.")
        
    def update(self, key: str, value: str) -> None:
        if self.redis.exists(key):
            self.redis.delete(key)
            self.redis.set(key, value)
        else:
            self.redis.set(key, value)
    
    def delete(self, key: str) -> None:
        if self.redis.exists(key):
            self.redis.delete(key)
            return
        
        raise Exception(f"Key {key} does not exist.")
            
    def get_automl_job_ids(self) -> list:
        cursor = '0'
        matching_keys = []
        
        while cursor != 0:
            cursor, keys = self.redis.scan(cursor = cursor)
            
            for key in keys:
                if key.startswith(CELERY_KEY_PREFIX):
                    matching_keys.append(key.replace(CELERY_KEY_PREFIX, ""))
                    
        return matching_keys
        
    def get_keys_by_pattern(self, pattern: str) -> tuple:
        cursor = '0'
        redis_keys = []
        key_values = []

        while cursor != 0:
            cursor, keys = self.redis.scan(cursor=cursor, match=pattern)
            
            for key in keys:
                value = self.get(key)
                
                redis_keys.append(key)
                key_values.append(value)

        return (redis_keys, key_values)
            
    def generate_unique_job_key(self) -> str:
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{unique_id}-{timestamp}"

    def __del__(self) -> None:
        print("Redis client destroyed.")
        self.redis.close()