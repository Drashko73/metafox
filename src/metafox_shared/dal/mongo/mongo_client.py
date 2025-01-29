import os
from datetime import datetime
from dotenv import load_dotenv

from pymongo import MongoClient as PyMongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from metafox_shared.dal.idatastore import IDataStore

class MongoClient(IDataStore):
    def __init__(self) -> None:
        load_dotenv()
        
        self.client: PyMongoClient = PyMongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
        self.db: Database = self.client.get_database(os.getenv("MONGO_DB", "metafox"))
        
        print("MongoDB connection established.")
    
    def set(self, key: str, value: str, collection_name: str) -> None:
        collection = self.__get_collection(collection_name)
        collection.insert_one({
            "_id": key, 
            "value": value, 
            "created_at": datetime.now()
        })

    def get(self, key: str, collection_name: str) -> str:
        collection = self.__get_collection(collection_name)
        document = collection.find_one({"_id": key})
        return document["value"] if document else None

    def update(self, key: str, value: str, collection_name: str) -> None:
        collection = self.__get_collection(collection_name)
        collection.update_one({"_id": key}, {"$set": {"value": value}})

    def delete(self, key: str, collection_name: str) -> None:
        collection = self.__get_collection(collection_name)
        collection.delete_one({"_id": key})

    def get_automl_job_ids(self, collection_name: str) -> list:
        collection = self.__get_collection(collection_name)
        return [doc["_id"] for doc in collection.find({}, {"_id": 1})]

    def get_keys_by_pattern(self, pattern: str, collection_name) -> list:
        collection = self.__get_collection(collection_name)
        regex_pattern = f".*{pattern}.*"
        return [doc["_id"] for doc in collection.find({"_id": {"$regex": regex_pattern}})]
    
    def close(self) -> None:
        print("Closing MongoDB connection...")
        self.client.close()
        
    def __get_collection(self, collection_name: str) -> Collection:
        return self.db.get_collection(collection_name)