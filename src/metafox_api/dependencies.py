from fastapi import Depends
from metafox_shared.dal.mongo.mongo_client import MongoClient
from metafox_api.controllers.general_controller import GeneralController
from metafox_api.controllers.tpot_controller import TPOTController

mongo_client_instance: MongoClient = None

def get_mongo_client() -> MongoClient:
    global mongo_client_instance
    if mongo_client_instance is None:
        mongo_client_instance = MongoClient()
    return mongo_client_instance

def get_general_controller(mongo_client: MongoClient = Depends(get_mongo_client)) -> GeneralController:
    return GeneralController(mongo_client)

def get_tpot_controller(mongo_client: MongoClient = Depends(get_mongo_client)) -> TPOTController:
    return TPOTController(mongo_client)