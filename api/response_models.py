from typing import List, Optional
from pydantic import BaseModel


class ActivityQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None


class ActivityResponse(BaseModel):
    status: str
    questions: list[ActivityQuestion]

class EvaluationResponse(BaseModel):
    score: int
    feedback: str
    correct_answer: str