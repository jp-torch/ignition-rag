CREATE TABLE documents (
    id TEXT PRIMARY KEY,
	source TEXT,
	file_bytes BYTEA,
	user_id TEXT,
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);