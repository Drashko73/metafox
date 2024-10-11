from abc import ABC, abstractmethod
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from metafox_shared.utilis import get_current_date

class AutoMLJob(BaseModel, ABC):
    job_name: Annotated[Optional[str], Field(
        default=None,
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
    timestamp_created: Annotated[datetime, Field(
        default_factory=get_current_date,
        description="Timestamp when the job was created"
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