import uuid

def initTables():
	queries = [
		"Exchange/Ignition RAG/Init/Create Chats Table",
		"Exchange/Ignition RAG/Init/Create Messages Table",
		"Exchange/Ignition RAG/Init/Create Documents Table",
		"Exchange/Ignition RAG/Init/Vector Extension",
		"Exchange/Ignition RAG/Init/Create Embeddings Table",
		"Exchange/Ignition RAG/Init/Create Embeddings Index"
	]
	for query in queries:
		print("Running query %s" % query)
		system.db.execUpdate(query, {})
		
	print("All tables created!")
	
def getId():
	return str(uuid.uuid4())