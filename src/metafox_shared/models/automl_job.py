from abc import ABC, abstractmethod
from typing import Annotated
from pydantic import BaseModel, Field

class AutoMLJob(BaseModel, ABC):
    job_name: Annotated[str, Field(
        description="Job name"
    )]
    data_source: Annotated[str, Field(
        description="Data source"
    )]
    target_variable: Annotated[str, Field(
        description="Target variable"
    )]
    problem_type: Annotated[str, Field(
        description="Problem type"
    )]
    
    @abstractmethod
    def custom_model_dump(self) -> dict:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass