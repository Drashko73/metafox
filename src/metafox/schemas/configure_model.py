from typing import Union
from pydantic import BaseModel
from pydantic.networks import HttpUrl

class ConfigureModel(BaseModel):
    name: Union[str, None]
    data_source: Union[str, HttpUrl]
    target_variable: str
    model_type: str
    random_state: Union[int, None]
    model: str
    max_iter: Union[int, None]
    timeout: Union[int, None]
    automl_library: str = "tpot"