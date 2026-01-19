CREATE TABLE document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    page INTEGER,
    chunk INTEGER,
    text TEXT NOT NULL,
    embedding VECTOR(768), -- change dimension if needed
    source TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);