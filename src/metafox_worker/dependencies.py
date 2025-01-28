from metafox_shared.dal.mongo.mongo_client import MongoClient

mongo_client_instance = None

def get_mongo_client():
    global mongo_client_instance
    if mongo_client_instance is None:
        mongo_client_instance = MongoClient()
    return mongo_client_instance