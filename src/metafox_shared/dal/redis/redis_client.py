import os
import uuid

from redis import Redis
from datetime import datetime
from dotenv import load_dotenv
from metafox_shared.dal.idatastore import IDataStore

class RedisClient (IDataStore):
    def __init__(self) -> None:
        load_dotenv()
        self.redis = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0),
            decode_responses=True,
        )
        
    def set(self, key: str, value: str) -> None:
        if self.redis.exists(key):
            raise Exception(f"Key {key} already exists.")
        
        self.redis.set(key, value)
        
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
        
        raise Exception(f"Key {key} does not exist.")
            
    def get_all_keys(self) -> list:
        return self.redis.keys("[^celeryid_]*")
            
    def generate_unique_job_key(self) -> str:
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{unique_id}_{timestamp}"

    def __del__(self) -> None:
        print("Redis client destroyed.")
        self.redis.close()