from fastapi import FastAPI

from api.request_models import ActivityRequest, EvaluationRequest
from api.response_models import ActivityResponse, EvaluationResponse
from mcp_server.google_drive import read_google_drive
from mcp_server.google_drive import search_pdf, read_google_drive

from workflow.workflow_manager import WorkflowManager

app = FastAPI(
    title="AI Activity Generation API",
    version="1.0.0",
    description="AI Multi-Agent Educational Platform"
)

workflow = WorkflowManager()


@app.get("/")
def home():
    return {
        "message": "AI Activity Generation API"
    }


@app.post(
    "/generate-activity",
    response_model=ActivityResponse
)
def generate_activity(request: ActivityRequest):

    file_id = search_pdf(
        request.subject,
        request.topic
    )

    lesson = read_google_drive(file_id)

    questions = workflow.run(
        lesson,
        request.activityType,
        request.numberOfQuestions
    )

    for q in questions:
        q["type"] = request.activityType

    return ActivityResponse(
        status="SUCCESS",
        activityType=request.activityType,
        questions=questions
    )

def generate_activity(request: ActivityRequest):
    file_id = search_pdf(
        request.subject,
        request.topic
    )

    lesson = read_google_drive(file_id)

    #call workflow object run method
    questions = workflow.run(
        lesson,
        request.activityType,
        request.numberOfQuestions
    )

    for q in questions:
        q["type"] = request.activityType

    return ActivityResponse(
        status="SUCCESS",
        activityType=request.activityType,
        questions=questions
    )
@app.post("/evaluate-answer")
def evaluate_answer(request: EvaluationRequest):

    result = workflow.evaluate(
        request.student_answer,
        request.correct_answer
    )

    return EvaluationResponse(
        score=result.score,
        feedback=result.feedback,
        correct_answer=request.correct_answer
    )
