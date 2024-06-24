
from pydantic import BaseModel

class StartAutoMLRequest(BaseModel):
    link_to_data: str
    target: str