import re

from pdf_reader import read_pdf
from workflow.workflow_manager import WorkflowManager


def extract_answer(question_text):
	match = re.search(r"^Answer:\s*(.+)$", question_text, re.MULTILINE)
	if match:
		return match.group(1).strip()
	return question_text.strip()

lesson = read_pdf("content_analysis_agent/pdfs/science.pdf")

workflow = WorkflowManager()

# Run the first three agents
generated_question, validation_result = workflow.run(lesson)
print("--------------------------------")

# Student's answer
student_answer = "Chlorophyll"
correct_answer = extract_answer(generated_question)
# Run the Answer Evaluation Agent
workflow.evaluate(student_answer, correct_answer)