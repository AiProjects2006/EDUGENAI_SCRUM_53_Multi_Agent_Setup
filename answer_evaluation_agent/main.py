from agent.answer_evaluation_agent import AnswerEvaluationAgent
from strategies.mcq_strategy import MCQStrategy
from strategies.fill_blank_strategy import FillBlankStrategy

# -------------------------
# MCQ Evaluation
# -------------------------

agent = AnswerEvaluationAgent(MCQStrategy())

result = agent.evaluate(
    "B",
    "B"
)

print("MCQ")
print(result.score)
print(result.feedback)

print("----------------------")

# -------------------------
# Fill in the Blank
# -------------------------

agent.set_strategy(FillBlankStrategy())

result = agent.evaluate(
    "chlorophyll",
    "chlorophyll"
)

print("Fill Blank")
print(result.score)
print(result.feedback)