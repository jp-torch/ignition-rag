def pullModel(server, model):
	"""Pulls the given ollama model to the server
	
	Args:
	    server (str): Path to ollama server
	    model (str): Name of model to pull
	"""
	payload = {
		"name": model
	}
	
	headers = {
		"Content-Type": "application/json"
	}
	
	client = system.net.httpClient()
	response = client.post(
		server + "/api/pull",
		headers=headers,
		data=system.util.jsonEncode(payload)
	)
	
	if response.isClientError():
		raise Exception("Error when pulling the model")

def getEmbeddings(text, timeout=5000):
	"""Generate the vector embeddings for the given text
	
	Args:
	    text (str): Text to generate embeddings for
	    timeout (optional int): timeout for tag reading
	
	Returns:
	    List: List of floats
	"""
	tagPaths = [
		"[default]Exchange/IgnitionRAG/OllamaServer",
		"[default]Exchange/IgnitionRAG/EmbeddingModel"
	]

	ollamaData = system.tag.readBlocking(tagPaths, timeout)
	server = ollamaData[0].value.rstrip("/")
	model = ollamaData[1].value
	
	pullModel(server, model)

	payload = {
		"model": model,
		"prompt": text
	}

	headers = {
		"Content-Type": "application/json"
	}

	client = system.net.httpClient(timeout=timeout)

	response = client.post(
		server + "/api/embeddings",
		headers=headers,
		data=system.util.jsonEncode(payload)
	)
	if response.isClientError():
		raise Exception("Error generating the vector embeddings")

	result = system.util.jsonDecode(response.getText())
	return [float(x) for x in result["embedding"]]

def getAnswer(text, timeout=5000):
	"""Generate the answer for the given text
	
	Args:
	    text (str): Text to generate answer for
	    timeout (optional int): timeout for tag reading
	
	Returns:
	    str: Answer to question
	"""
	tagPaths = [
		"[default]Exchange/IgnitionRAG/OllamaServer",
		"[default]Exchange/IgnitionRAG/AnswerModel"
	]
	
	ollamaData = system.tag.readBlocking(tagPaths, timeout)
	server = ollamaData[0].value.rstrip("/")
	model = ollamaData[1].value
	
	pullModel(server, model)
	
	payload = {
		"model": model,
		"prompt": text,
		"stream": False
	}

	headers = {
		"Content-Type": "application/json"
	}

	client = system.net.httpClient(timeout=timeout)

	response = client.post(
		server + "/api/generate",
		headers=headers,
		data=system.util.jsonEncode(payload)
	)
	if response.isClientError():
		raise Exception("Error generating the answer for the given question")

	result = system.util.jsonDecode(response.getText())
	return result.get("response", "").strip()