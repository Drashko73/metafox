from metafox_shared.dal.idatastore import IDataStore
import uuid

class InMemoryDataStore(IDataStore):
    
    def __init__(self) -> None:
        self.store = {}
        
    def get(self, key: str) -> str:
        return self.store.get(key)
    
    def set(self, key: str, value: str) -> None:
        self.store[key] = value
    
    def delete(self, key: str) -> None:
        if key in self.store:
            del self.store[key]
            
    def generate_unique_job_key(self, prefix: str) -> str:
        unique_key = prefix + str(uuid.uuid4())
        return unique_key
    
    def __del__(self):
        self.store.clear()