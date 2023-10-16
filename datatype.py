from pydantic import BaseModel

class PostRequest(BaseModel):
    title: str
    description: str
    createdBy: str
    category: str
