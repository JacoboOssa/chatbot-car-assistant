import uuid
from typing import Optional
from pydantic import BaseModel, Field
from .requests import Question

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    email: str
    password: str
    requests: Optional[list[Question]] = []
    
    