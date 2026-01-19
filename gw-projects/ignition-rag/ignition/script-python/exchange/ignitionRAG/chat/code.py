from exchange.ignitionRAG.ollama import getAnswer
from exchange.ignitionRAG.prompts import QUESTION_TITLE_PROMPT

def generateChatTitle(question):
	"""Returns a title for a new chat
	
	Args:
	    question (str): First question of the new chat.
	
	Returns:
	    str: The title for the new chat
	"""
	prompt = QUESTION_TITLE_PROMPT.format(question=question)
	title = getAnswer(prompt)
	return title