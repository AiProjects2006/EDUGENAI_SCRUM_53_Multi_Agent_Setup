from pydantic import BaseModel


class ActivityRequest(BaseModel):
    subject: str
    topic: str
    activityType: str
    numberOfQuestions: int


class EvaluationRequest(BaseModel):
    student_answer: str
    correct_answer: str
