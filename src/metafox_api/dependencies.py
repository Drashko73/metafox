import os

from fastapi import Depends
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.dal.mongo.mongo_client import MongoClient
from metafox_shared.dal.redis.redis_client import RedisClient
from metafox_api.controllers.general_controller import GeneralController
from metafox_api.controllers.tpot_controller import TPOTController

mongo_client_instance: MongoClient = None
redis_client_instance: RedisClient = None
db_client_instance: IDataStore = None

def __get_mongo_client() -> MongoClient:
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
    
    db_type = os.getenv("DB_TYPE", "mongo")
    
    if db_type == "redis":
        db_client_instance = _get_redis_client()
    elif db_type == "mongo":
        db_client_instance = __get_mongo_client()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return db_client_instance

def get_general_controller(mongo_client: MongoClient = Depends(get_data_store)) -> GeneralController:
    return GeneralController(mongo_client)

def get_tpot_controller(mongo_client: MongoClient = Depends(get_data_store)) -> TPOTController:
    return TPOTController(mongo_client)