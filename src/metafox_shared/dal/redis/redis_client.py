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
            """
            Set the value of a key in Redis.

            Args:
                key (str): The key to set.
                value (str): The value to set.

            Raises:
                Exception: If the key already exists in Redis.

            Returns:
                None
            """
            if self.redis.exists(key):
                raise Exception(f"Key {key} already exists.")
            
            self.redis.set(key, value)
        
    def get(self, key: str) -> str:
            """
            Retrieve the value associated with the given key from Redis.

            Args:
                key (str): The key to retrieve the value for.

            Returns:
                str: The value associated with the given key.

            Raises:
                Exception: If the key does not exist in Redis.
            """
            if self.redis.exists(key):
                return self.redis.get(key)
            
            raise Exception(f"Key {key} does not exist.")
    
    def delete(self, key: str) -> None:
            """
            Deletes a key from the Redis database.

            Args:
                key (str): The key to be deleted.

            Raises:
                Exception: If the key does not exist in the database.
            """
            if self.redis.exists(key):
                self.redis.delete(key)
            
            raise Exception(f"Key {key} does not exist.")
            
    def generate_unique_job_key(self, prefix: str) -> str:
        """
        Generates a unique job key with a given prefix, a UUID, and a timestamp.
        
        :param prefix: A string prefix to identify the job type.
        :return: A unique job key as a string.
        """
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}:{unique_id}:{timestamp}"

    def __del__(self) -> None:
        print("Redis client destroyed.")
        self.redis.close()