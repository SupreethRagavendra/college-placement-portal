# OpenRouter RAG Service for College Placement Portal

This directory contains the complete implementation of the OpenRouter RAG service for the College Placement Portal.

## Overview

The RAG (Retrieval-Augmented Generation) service provides intelligent chatbot functionality powered by OpenRouter AI models. It dynamically syncs with the Supabase database to provide up-to-date information about assessments, questions, and student performance.

## Key Features

1. **OpenRouter AI Integration**: Uses Qwen and DeepSeek models with automatic fallback
2. **Dynamic Knowledge Sync**: Automatically updates when admin adds assessments/data
3. **Student Data Privacy**: Each student sees only their own data
4. **Laravel Integration**: Seamless integration with existing Laravel application
5. **Comprehensive Testing**: Includes test scripts and validation tools

## Directory Structure

```
python-rag/
├── main.py                 # Main FastAPI service
├── openrouter_client.py    # OpenRouter API wrapper
├── knowledge_sync.py       # Database sync logic
├── context_handler.py      # Query processing and context building
├── response_formatter.py   # Response formatting
├── init_knowledge.py       # Initial knowledge builder
├── incremental_sync.py     # Incremental update system
├── test_rag.py             # Testing script
├── requirements.txt        # Python dependencies
├── .env                   # Configuration file
├── start_rag_service.sh    # Startup script
├── test_setup.sh          # Setup validation script
├── RAG_SETUP.md           # Setup guide
├── RAG_ARCHITECTURE.md    # Architecture documentation
├── OPENROUTER_GUIDE.md    # OpenRouter usage guide
└── TROUBLESHOOTING.md     # Troubleshooting guide
```

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Update the `.env` file with your OpenRouter API key and database credentials.

3. **Start the Service**:
   ```bash
   ./start_rag_service.sh
   ```

4. **Test the Setup**:
   ```bash
   ./test_setup.sh
   ```

## API Endpoints

- `POST /chat` - Handle student queries with RAG
- `POST /sync-knowledge` - Trigger knowledge base update
- `GET /health` - Health check
- `POST /init-student-context` - Initialize student-specific context
- `GET /models` - List available models

## Documentation

- [RAG_SETUP.md](RAG_SETUP.md) - Complete setup instructions
- [RAG_ARCHITECTURE.md](RAG_ARCHITECTURE.md) - System architecture
- [OPENROUTER_GUIDE.md](OPENROUTER_GUIDE.md) - OpenRouter API usage
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## Security

- Student data isolation is maintained
- API keys are stored securely in environment variables
- Service only accepts requests from localhost

## Performance

- Implements caching for improved response times
- Includes fallback mechanisms for reliability
- Optimized database queries for efficient data retrieval