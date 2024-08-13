from abc import ABC, abstractmethod
from typing import Annotated
from pydantic import BaseModel, Field, field_validator

class AutoMLJob(BaseModel, ABC):
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
    
    # Field validators
    @field_validator('problem_type')
    def check_problem_type(cls, value):
        if value not in ['classification', 'regression']:
            raise ValueError('Problem type must be either classification or regression')
        return value