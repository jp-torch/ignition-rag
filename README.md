## Ignition RAG

A simple Retrieval-Augmented Generation (RAG) project built on Ignition by Inductive Automation.

## What is RAG?

RAG (Retrieval-Augmented Generation) is a pattern that helps an LLM answer questions using **your documents**:

- **Retrieve**: split documents into chunks, embed them, then run a similarity search to find the most relevant chunks for a question.
- **Augment**: include those chunks as context (and often citations/metadata).
- **Generate**: have the LLM draft an answer grounded in that retrieved context.

Compared to “chatting with a model” alone, RAG typically produces **more accurate, more verifiable** answers because it can quote and reference the source material.

## Spin up the environment

- **Prereqs**: Docker + Docker Compose
- **Start**:

```bash
docker compose up --build -d
```

- **Stop**:

```bash
docker compose down
```

- **Delete Data**:
```bash
docker compose down -v
```

Notes:
- `sql-init/` contains the database initialization scripts.
- `gw-projects/` contains the Ignition project resources (Perspective, scripts, named queries, etc.).

## Access & Configuration

- **Gateway**: Once running, access the Ignition Gateway at `http://localhost:8088`
- **Ollama Models**: Configure which models to use via tags in the Ignition Gateway:
  - `Exchange/IgnitionRAG/OllamaServer` - Ollama server URL (default: `http://ollama:11434`)
  - `Exchange/IgnitionRAG/EmbeddingModel` - Model for generating embeddings (default: `nomic-embed-text`)
  - `Exchange/IgnitionRAG/AnswerModel` - Model for generating answers (default: `nomic-embed-text`)

  Change these tags in the Gateway to use different Ollama models (e.g., `llama3`, `mistral`, etc.).

## Contributing

- **Branch**: create a feature branch off `main`
- **Style**: keep changes small and scoped; prefer clear names and comments over cleverness
- **Ignition resources**: changes typically live under `gw-projects/` (project assets) and `gw-config/` (gateway config)
- **PRs**: include a short description + how you validated the change (screenshots welcome for Perspective)

## Future updates / ideas

- **OpenAI integration** (in addition to local models), with per-environment configuration
- **Support for more document types** (Word, Excel, etc.)
- **Per-chat document selection** (choose which documents are in-scope for a given conversation)
- **Better citation UX** (show sources + jump-to-chunk)
- **Improved chunking/metadata** (title/section detection, tags, document versions)
