from pydantic import BaseModel

class RetrievedContext(BaseModel):
    content: str
    score: float
    source: str
