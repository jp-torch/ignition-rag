INSERT INTO document_chunks
(id, document_id, page, chunk, text, embedding)
VALUES
(:id, :documentId, :page, :chunk, :text, CAST(:embedding AS vector))