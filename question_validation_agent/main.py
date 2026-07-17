from agent.question_validation_agent import QuestionValidationAgent

from strategies.grammar_validation_strategy import GrammarValidationStrategy
from strategies.duplicate_validation_strategy import DuplicateValidationStrategy

questions = [

"What is Photosynthesis?",

"What is Photosynthesis?",

"Plants use ________ to absorb sunlight.",

"Which pigment absorbs sunlight?"
]

# Grammar Validation


agent = QuestionValidationAgent(
    GrammarValidationStrategy()
)

result = agent.validate(questions)

print("Grammar Validation")
print("-----------------------")
print(result.feedback)

print()


# Duplicate Validation

agent.set_strategy(
    DuplicateValidationStrategy()
)

result = agent.validate(questions)

print("Duplicate Validation")
print("-----------------------")
print(result.feedback)