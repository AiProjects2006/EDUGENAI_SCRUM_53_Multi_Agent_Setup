from pdf_reader import read_pdf
from agent.content_analysis_agent import ContentAnalysisAgent
from strategies.pdf_strategy import PDFAnalysisStrategy
from strategies.text_strategy import TextAnalysisStrategy

lesson = read_pdf("pdfs/science.pdf")


agent = ContentAnalysisAgent(PDFAnalysisStrategy())

result = agent.analyze(lesson)

print(result)

agent.set_strategy(TextAnalysisStrategy())

result = agent.analyze(lesson)

print(result)