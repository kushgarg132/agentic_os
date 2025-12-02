# Agentic AI Operating System

A fully autonomous Agentic AI Operating System with complete Google data access, multi-agent architecture, and voice integration.

## Features
- **Full Google Data Access**: Gmail, Drive, Docs, Calendar, Contacts.
- **Multi-Agent Architecture**: Executive, Email, Knowledge, Planner agents.
- **RAG & Knowledge Graph**: Advanced memory and retrieval.
- **Voice Interface**: Google Assistant integration.
- **Automations**: Daily and weekly summaries.

## Setup
1. **Environment Variables**: Copy `.env.example` to `.env` and fill in the values.
2. **Google Cloud**: Setup a project and download `client_secrets.json`.
3. **Docker**: Run `docker-compose up --build`.

## Development
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **AI**: LangChain + LangGraph

## Folder Structure
- `/auth`: OAuth and token management.
- `/agents`: AI agents implementation.
- `/tools`: LangChain tools for Google services.
- `/rag`: RAG system (Chunking, Embedding, Retrieval).
- `/knowledge_graph`: Neo4j/Postgres graph builder.
- `/services`: Wrappers for Google APIs.
