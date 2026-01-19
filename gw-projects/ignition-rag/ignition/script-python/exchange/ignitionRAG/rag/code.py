import uuid
import re
from exchange.ignitionRAG.ollama import getEmbeddings, getAnswer
from exchange.ignitionRAG.pdf import getText
from exchange.ignitionRAG.prompts import RAG_ANSWER_STRICT_PROMPT
from java.lang import String

NUM_RELATED_CHUNKS = 10

def cleanText(text):
	"""Clean the given text
	
	Args:
	    text (str): Text to clean
	
	Returns:
	    str: Cleaned text
	"""
	text = text.replace("\r", " ").replace("\n", " ")
	text = re.sub(r"\s+", " ", text)
	return text.strip()
	
def chunkText(text, chunkSize=1000, overlap=200):
	"""Chunk the text into smaller portions
	
	Args:
	    text (str): Text to chunk
	    chunkSize (optional int): Number of characters in each chunk
	    overlap (optional int): The number of character overlap between chunks
	
	Returns:
	    List: List of text chunks
	"""
	chunks = []
	start = 0
	textLength = len(text)
	
	while start < textLength:
		end = start + chunkSize
		chunk = text[start:end]
		chunks.append(chunk)
		
		start = end - overlap
		if start < 0:
			start = 0
			
	return chunks
	
def loadData(documentId, fileBytes, fileName, tx=None):	
	"""Generate the embeddings for the document and store in DB
	
	Args:
	    documentId (str): ID from the documents table
	    fileBytes (str): Byte representation of doc
	    fileName (str): Name of file
	    tx (optional str): DB transaction
	"""
	queryPath = "Exchange/Ignition RAG/Insert Embedding"
	
	# ---------- PDF ----------
	if fileName.endswith(".pdf"):
		pageData = getText(fileName, fileBytes)
		
		for page in pageData:
			cleanedText = cleanText(page["text"])
			chunks = chunkText(cleanedText)
			
			for i, chunk in enumerate(chunks):
				embeddings = getEmbeddings(chunk)
				params = {
					"id": "{}_p{}_c{}".format(documentId, page["page"], i),
					"documentId": documentId,
					"page": page["page"],
					"chunk": i,
					"text": chunk,
					"embedding": embeddings,
				}
				system.db.execUpdate(queryPath, params, tx=tx)

	# ---------- TXT ----------
	elif fileName.endswith(".txt"):
		text = String(fileBytes, "UTF-8")
		
		cleanedText = cleanText(text)
		chunks = chunkText(cleanedText)
		
		for i, chunk in enumerate(chunks):
			embeddings = getEmbeddings(chunk)
			params = {
				"id": "{}_c{}".format(documentId, i),
				"documentId": documentId,
				"page": 1,
				"chunk": i,
				"text": chunk,
				"embedding": embeddings,
			}
			
			system.db.execUpdate(queryPath, params, tx=tx)

def generateAnswer(question):
	"""Fetch the related chunks for the quetions and generate an answer to the question
	
	Args:
	    question (str): TQuestions to generate an answer for
	
	Returns:
	    str: Answer to question
	"""
	questionEmbeddings = getEmbeddings(question)
	
	# Get the related doc chunks
	chunks = system.db.execQuery(
		"Exchange/Ignition RAG/Get Related Chunks", 
		{"limit": NUM_RELATED_CHUNKS, "queryEmbedding": questionEmbeddings}
	)
	# Build the context from the chunks
	context = []
	for row in chunks:
		context.append({
			"page": row["page"],
			"chunk": row["chunk"],
			"text": row["text"],
			"source": row["source"],
			"similarity": row["similarity"]
		})
	# Get the answer for the question
	prompt = RAG_ANSWER_STRICT_PROMPT.format(
	    context=context,
	    question=question
	)
	answer = getAnswer(prompt)
	return answer	