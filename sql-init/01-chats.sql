CREATE TABLE chats (
    id TEXT PRIMARY KEY,
    chat_title TEXT,
    user_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);