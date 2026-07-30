from fastapi import FastAPI

from api.request_models import ActivityRequest, EvaluationRequest
from api.response_models import ActivityResponse, ActivityQuestion, EvaluationResponse
from content_analysis_agent.pdf_reader import read_pdf

from workflow.workflow_manager import WorkflowManager

app = FastAPI(
    title="AI Activity Generation API",
    version="1.0.0",
    description="AI Multi-Agent Educational Platform"
)

workflow = WorkflowManager()


@app.post("/")
def home():
    return {
        "message": "AI Activity Generation API"
    }


@app.post(
    "/generate-activity",
    response_model=ActivityResponse
)
def generate_activity(request: ActivityRequest):
    if request.subject == "Science":
        lesson = read_pdf("content_analysis_agent/pdfs/science.pdf")
    elif request.subject == "Maths":
        lesson = read_pdf("content_analysis_agent/pdfs/maths.pdf")
    else:
        lesson = read_pdf("content_analysis_agent/pdfs/default.pdf")

    questions = workflow.run(
        lesson,
        request.activityType,
        request.numberOfQuestions
    )

    return ActivityResponse(
        status="SUCCESS",
        questions=[
            ActivityQuestion(
                question=q.get("question", ""),
                options=q.get("options", []),
                answer=q.get("answer", "")
            )
            for q in questions
        ]
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