from content_analysis_agent.agent.content_analysis_agent import ContentAnalysisAgent
from question_generation_agent.agent.question_generation_agent import QuestionGenerationAgent
from question_validation_agent.agent.question_validation_agent import QuestionValidationAgent
from answer_evaluation_agent.agent.answer_evaluation_agent import AnswerEvaluationAgent

from content_analysis_agent.strategies.pdf_strategy import PDFAnalysisStrategy

from question_generation_agent.strategies.mcq_strategy import MCQStrategy

from question_validation_agent.strategies.grammar_validation_strategy import GrammarValidationStrategy

from answer_evaluation_agent.strategies.mcq_strategy import MCQStrategy as EvaluationStrategy


class WorkflowManager:

    def __init__(self):

        self.content_agent = ContentAnalysisAgent(
            PDFAnalysisStrategy()
        )

        self.question_agent = QuestionGenerationAgent(
            MCQStrategy()
        )

        self.validation_agent = QuestionValidationAgent(
            GrammarValidationStrategy()
        )

        self.answer_agent = AnswerEvaluationAgent(
            EvaluationStrategy()
        )

    def run(self, lesson):

        # Content Analysis Agent
        print("========== Content Analysis Agent ==========")

        analysis = self.content_agent.analyze(lesson)

        print(analysis)

        print("--------------------------------")

        # Question Generation Agent

        print("========== Question Generation Agent ==========")

        questions = self.question_agent.generate(analysis)

        print(questions)

        print("--------------------------------")

        # Question Validation Agent

        print("========== Question Validation Agent ==========")

        validated_questions = self.validation_agent.validate(
            questions
        )

        print(validated_questions)

        print("--------------------------------")

        return questions, validated_questions

    def evaluate(self, student_answer, correct_answer):
        print("========== Answer Evaluation Agent ==========")

        result = self.answer_agent.evaluate(
            student_answer,
            correct_answer
        )

        print("Student Answer :", student_answer)
        print("Correct Answer :", correct_answer)
        print("Score :", result.score)
        print("Feedback :", result.feedback)

        return result