# RAG Service Setup Guide

This guide provides complete instructions for setting up the OpenRouter RAG service for the College Placement Portal.

## Prerequisites

1. Python 3.8 or higher
2. PostgreSQL database (Supabase)
3. OpenRouter API key
4. Laravel application running

## Installation Steps

### 1. Install Python Dependencies

Navigate to the python-rag directory and install the required packages:

```bash
cd python-rag
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `python-rag` directory with the following configuration:

```env
# OpenRouter API
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free

# Supabase Database
SUPABASE_DB_HOST=your-supabase-host.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=your-database-name
SUPABASE_DB_USER=your-database-user
SUPABASE_DB_PASSWORD=your-database-password

# Service Configuration
SERVICE_PORT=8001
LOG_LEVEL=INFO
```

### 3. Configure Laravel Environment

Update your Laravel `.env` file with the following RAG service configuration:

```env
# RAG Service Configuration
RAG_SERVICE_URL=http://localhost:8001
RAG_API_KEY=your-secure-internal-api-key

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free

# Supabase Configuration for RAG
SUPABASE_DB_HOST=your-supabase-host.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=your-database-name
SUPABASE_DB_USER=your-database-user
SUPABASE_DB_PASSWORD=your-database-password
```

### 4. Update Laravel Configuration

Ensure your `config/rag.php` file is updated with the OpenRouter settings as shown in the previous section.

### 5. Start the RAG Service

Run the RAG service using:

```bash
cd python-rag
python main.py
```

Or use the provided startup script:

```bash
chmod +x start_rag_service.sh
./start_rag_service.sh
```

### 6. Test the Setup

Run the test script to verify all components are working:

```bash
cd python-rag
python test_rag.py
```

## Service Endpoints

The RAG service exposes the following endpoints:

- `POST /chat` - Handle student queries with RAG
- `POST /sync-knowledge` - Trigger knowledge base update
- `GET /health` - Health check
- `POST /init-student-context` - Initialize student-specific context
- `GET /models` - List available models

## Integration with Laravel

The Laravel ChatbotController automatically integrates with the RAG service. No additional configuration is needed after setting the environment variables.

## Automatic Sync

The system automatically syncs knowledge when:
- New assessments are created, updated, or deleted
- New questions are added, updated, or deleted
- Assessment status is changed

## Troubleshooting

If you encounter issues:

1. Check that all environment variables are correctly set
2. Verify database connectivity
3. Ensure the RAG service is running on the correct port
4. Check logs in `rag_service.log` for detailed error information

## Security Considerations

- Keep your OpenRouter API key secure
- The RAG service should only be accessible from localhost or trusted networks
- Student data is isolated and secure
- All communication between Laravel and RAG service should be over localhost

## Performance Optimization

- The service includes caching for improved performance
- Database connections are properly managed
- API calls include appropriate timeouts
- Fallback mechanisms ensure reliability