from typing import List
from pydantic import BaseModel

class CreateAutoMLJob(BaseModel):
    """
    Represents a request to create an AutoML job.

    Args:
        job_name (str): The name of the job.
        data_source (str): The data source for the job.
        target_variable (str): The target variable for the job.
        model_type (str): The type of model to be used.
        metrics (List[str]): The evaluation metrics for the job.
        random_seed (int): The random seed for reproducibility.
        model (str): The model to be used for the job.
        max_iterations (int): The maximum number of iterations for the job.
        timeout (int): The timeout for the job.
    """
    job_name: str
    data_source: str
    target_variable: str
    model_type: str
    metrics: List[str]
    random_state: int
    model: str
    max_iterations: int
    timeout: int
    automl_library: str