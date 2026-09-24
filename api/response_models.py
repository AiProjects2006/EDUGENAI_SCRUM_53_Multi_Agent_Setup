from typing import List, Dict, Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field


# ---------------- MCQ ----------------

class MCQQuestion(BaseModel):
    type: Literal["MCQ"] = "MCQ"
    question: str
    options: List[str]
    answer: str


# ---------------- Fill Blank ----------------

class FillBlankQuestion(BaseModel):
    type: Literal["FillBlank"] = "FillBlank"
    question: str
    answer: str


# ---------------- Matching ----------------

class MatchItem(BaseModel):
    id: str
    text: str


class MatchingQuestion(BaseModel):
    type: Literal["Matching"] = "Matching"
    question: str
    leftItems: List[MatchItem]
    rightItems: List[MatchItem]
    answers: dict[str, str]


# ---------------- Sorting ----------------

class SortingQuestion(BaseModel):
    type: Literal["Sorting"] = "Sorting"

    question: str

    sortMode: Literal["sequence", "category"]

    items: List[str]

    # Used when sortMode = sequence
    correctOrder: Optional[List[str]] = None

    # Used when sortMode = category
    correctGroups: Optional[Dict[str, List[str]]] = None


# ---------------- Drag Drop ----------------

class DragDropItem(BaseModel):
    id: str
    text: str


class DragDropTarget(BaseModel):
    id: str
    text: str


class DragDropQuestion(BaseModel):
    type: Literal["DragDrop"] = "DragDrop"
    question: str
    items: List[DragDropItem]
    targets: List[DragDropTarget]
    answers: dict[str, str]


# ---------------- Poll ----------------

class PollQuestion(BaseModel):
    type: Literal["Poll"] = "Poll"
    question: str
    options: List[str]
    correctAnswer: str
    graded: bool = False

class ShortAnswerQuestion(BaseModel):
    type: Literal["ShortAnswer"] = "ShortAnswer"
    question: str
    expectedAnswer: str
    keywords: List[str]

class HotspotQuestion(BaseModel):
    type: Literal["Hotspot"] = "Hotspot"
    question: str
    imageDescription: str
    correctRegion: str
    feedback: str

class ProblemSolvingQuestion(BaseModel):
    type: Literal["ProblemSolving"] = "ProblemSolving"
    question: str
    expectedAnswer: str
    solutionSteps: List[str]
    keywords: List[str]

class ApplicationBasedQuestion(BaseModel):
    type: Literal["ApplicationBased"] = "ApplicationBased"
    scenario: str
    question: str
    expectedAnswer: str
    keywords: List[str]

# -------- All supported activities --------

ActivityQuestion = Annotated[
    Union[
        MCQQuestion,
        FillBlankQuestion,
        MatchingQuestion,
        SortingQuestion,
        DragDropQuestion,
        PollQuestion,
        ShortAnswerQuestion,
        HotspotQuestion,
        ProblemSolvingQuestion,
        ApplicationBasedQuestion
    ],
    Field(discriminator="type")
]


class ActivityResponse(BaseModel):
    status: str
    activityType: str
    questions: List[ActivityQuestion]


class EvaluationResponse(BaseModel):
    score: int
    feedback: str
    correct_answer: str