from typing import List
from pydantic import BaseModel

class AutoMLJob(BaseModel):
    """
    Represents a request to create an AutoML job.

    Args:
        job_name (str): The name of the job.
        data_source (str): The data source for the job.
        target_variable (str): The target variable for the job.
        problem_type (str): The type of problem to be solved.
        metrics (List[str]): The evaluation metrics for the job.
        random_seed (int): The random seed for reproducibility.
        model (str): The model to be used for the job.
        max_iterations (int): The maximum number of iterations for the job.
        timeout (int): The timeout for the job.
    """
    job_name: str
    data_source: str
    target_variable: str
    problem_type: str
    metrics: List[str]
    random_state: int
    model: str
    max_iterations: int
    timeout: int
    automl_library: str
    
    def model_dump(self) -> dict:
        """
        Dumps the model details to a dictionary.
        
        Returns:
            dict: The model details.
        """
        return {
            "job_name": self.job_name,
            "data_source": self.data_source,
            "target_variable": self.target_variable,
            "problem_type": self.problem_type,
            "metrics": self.metrics,
            "random_state": self.random_state,
            "model": self.model,
            "max_iterations": self.max_iterations,
            "timeout": self.timeout,
            "automl_library": self.automl_library
        }
        
    def __str__(self) -> str:
        """
        Returns the string representation of the model details.
        
        Returns:
            str: The string representation of the model details.
        """
        return str(self.model_dump())