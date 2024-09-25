from abc import ABC, abstractmethod

class IDataStore(ABC):
    
    @abstractmethod
    def get(self, key: str) -> str:
        pass
    
    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        pass
    
    @abstractmethod
    def update(self, key: str, value: str) -> None:
        pass
    
    @abstractmethod
    def generate_unique_job_key(self) -> str:
        pass
    
    @abstractmethod
    def get_automl_job_ids(self) -> list:
        pass
    
    @abstractmethod
    def get_keys_by_pattern(self, pattern: str) -> list:
        pass
    
    @abstractmethod
    def __del__(self):
        pass