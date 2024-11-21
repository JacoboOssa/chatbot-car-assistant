import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Question(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    inputQuestion: str
    speceficproblem: str
    specificdiagnosis: str
    probability: float
    generalProblem: str
    generalDiagnosis: str
    createdAt: datetime = Field(default_factory=datetime.now)  # Agregar marca de tiempo

    
class QuestionRequest(BaseModel):
    question: str
    