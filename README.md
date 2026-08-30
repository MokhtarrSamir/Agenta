# RAG + MCP + Agent Student Assistant

Portfolio project: upload PDF lecture notes, then ask questions about them
using a RAG pipeline, MCP tools (web search), and an LLM.

- `Frontend/` — React + TypeScript + Vite app
- `Backend/` — FastAPI + MongoDB + Qdrant (currently: connectivity skeleton only)

## Prerequisites

- Docker and Docker Compose

## Run the backend (local)

1. Copy the environment template and adjust values:

   ```bash
   cp .env.example .env
   ```

2. Start all three services (MongoDB, Qdrant, FastAPI backend):

   ```bash
   docker compose up -d --build
   ```

3. Check everything is up:

   ```bash
   curl http://localhost:8000/api/v1/health
   # {"api":"ok","mongodb":"ok","qdrant":"ok"}
   ```

   Interactive API docs: `http://localhost:8000/docs`

4. Stop the stack:

   ```bash
   docker compose down
   ```

   To also delete the database volumes (fresh start):

   ```bash
   docker compose down -v
   ```