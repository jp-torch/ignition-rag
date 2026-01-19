SELECT
    id,
    document_id,
    page,
    chunk,
    text,
    source,
    1 - (embedding <=> CAST(:queryEmbedding AS vector)) AS similarity
FROM document_chunks
ORDER BY embedding <=> CAST(:queryEmbedding AS vector)
LIMIT :limit;