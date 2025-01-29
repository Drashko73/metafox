from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class IDataStore(ABC):
    @abstractmethod
    def set(self, key: str, value: str, collection_name: str) -> None:
        pass
    
    @abstractmethod
    def get(self, key: str, collection_name: str) -> str:
        pass
    
    @abstractmethod
    def update(self, key: str, value: str, collection_name: str) -> None:
        pass
    
    @abstractmethod
    def delete(self, key: str, collection_name: str) -> None:
        pass
    
    @abstractmethod
    def get_automl_job_ids(self, collection_name: str) -> list:
        pass
    
    @abstractmethod
    def get_keys_by_pattern(self, pattern: str, collection_name: str) -> list:
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass
    
    def generate_unique_job_key(self) -> str:
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{unique_id}-{timestamp}"