from pydantic import BaseModel

class StartAutoMLJob(BaseModel):
    """
    Represents a request to start an AutoML job.
    
    Args:
        job_name (str): The name of the job.
    """
    job_id: str