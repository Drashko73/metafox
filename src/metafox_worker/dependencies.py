from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.dal.mongo.mongo_client import MongoClient
from metafox_shared.dal.redis.redis_client import RedisClient
from metafox_shared.config import Config

mongo_client_instance = None
redis_client_instance = None
db_client_instance = None

def __get_mongo_client():
    global mongo_client_instance
    if mongo_client_instance is None:
        mongo_client_instance = MongoClient()
    return mongo_client_instance

def _get_redis_client():
    global redis_client_instance
    if redis_client_instance is None:
        redis_client_instance = RedisClient()
    return redis_client_instance

def get_data_store() -> IDataStore:
    global db_client_instance
    if db_client_instance is not None:
        return db_client_instance
    
    db_type = Config.DB_TYPE
    
    if db_type == "redis":
        db_client_instance = _get_redis_client()
    elif db_type == "mongo":
        db_client_instance = __get_mongo_client()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return db_client_instance