from content_analysis_agent.agent.content_analysis_agent import ContentAnalysisAgent
from question_generation_agent.agent.question_generation_agent import QuestionGenerationAgent
from question_validation_agent.agent.question_validation_agent import QuestionValidationAgent
from answer_evaluation_agent.agent.answer_evaluation_agent import AnswerEvaluationAgent

from content_analysis_agent.strategies.pdf_strategy import PDFAnalysisStrategy
from question_generation_agent.strategies.mcq_strategy import MCQStrategy
from question_generation_agent.strategies.fill_blank_strategy import FillBlankStrategy
from question_generation_agent.strategies.true_false_strategy import TrueFalseStrategy
from question_generation_agent.strategies.matching_strategy import MatchingStrategy
from question_generation_agent.strategies.sorting_strategy import SortingStrategy
from question_generation_agent.strategies.drag_drop_strategy import DragDropStrategy
from question_generation_agent.strategies.poll_strategy import PollStrategy
from question_generation_agent.strategies.short_answer_strategy import ShortAnswerStrategy
from question_generation_agent.strategies.hotspot_strategy import HotspotStrategy
from question_generation_agent.strategies.problem_solving_strategy import ProblemSolvingStrategy
from question_generation_agent.strategies.application_based_strategy import ApplicationBasedStrategy
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

    def run(self, lesson, activity_type, number_of_questions):

        # Content Analysis Agent
        #print("========== Content Analysis Agent ==========")

        analysis = self.content_agent.analyze(lesson)

        #print(analysis)
        #print("--------------------------------")

        # Question Generation Agent
        #print("========== Question Generation Agent ==========")

        # Select Strategy
        if activity_type == "MCQ":
            self.question_agent.strategy = MCQStrategy()

        elif activity_type == "FillInTheBlanks":
            self.question_agent.strategy = FillBlankStrategy()

        elif activity_type == "Matching":
            self.question_agent.set_strategy(MatchingStrategy())

        elif activity_type == "Sorting":
            self.question_agent.set_strategy(SortingStrategy())

        elif activity_type == "DragDrop":
            self.question_agent.set_strategy(DragDropStrategy())

        elif activity_type == "Poll":
            self.question_agent.set_strategy(PollStrategy())

        elif activity_type == "TRUE_FALSE":
            self.question_agent.strategy = TrueFalseStrategy()

        elif activity_type == "ShortAnswer":
            self.question_agent.set_strategy(ShortAnswerStrategy())

        elif activity_type == "Hotspot":
            self.question_agent.set_strategy(HotspotStrategy())

        elif activity_type == "ProblemSolving":
            self.question_agent.set_strategy(ProblemSolvingStrategy())

        elif activity_type == "ApplicationBased":
            self.question_agent.set_strategy(ApplicationBasedStrategy())

        else:
            raise ValueError(f"Unsupported activity type: {activity_type}")

        questions = self.question_agent.generate(
            analysis,
            number_of_questions
        )

        #print(questions)
        #print("--------------------------------")

        # Question Validation Agent
        #print("========== Question Validation Agent ==========")

        validated_questions = self.validation_agent.validate(
            questions
        )

        #print(validated_questions)
        #print("--------------------------------")

        return validated_questions

    def evaluate(self, student_answer, correct_answer):

        #print("========== Answer Evaluation Agent ==========")

        result = self.answer_agent.evaluate(
            student_answer,
            correct_answer
        )

        #print("Student Answer :", student_answer)
        #print("Correct Answer :", correct_answer)
        #print("Score :", result.score)
        #print("Feedback :", result.feedback)

        return result