#!/bin/bash

# Test Setup Script
# This script validates all connections for the RAG service

echo "Testing RAG Service Setup..."
echo "============================"

# Check if we're on Windows (Git Bash) or Linux/Mac
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3"
fi

# Test 1: Check Python dependencies
echo "1. Checking Python dependencies..."
if $PYTHON_CMD -c "import fastapi, uvicorn, requests, psycopg2, dotenv" 2>/dev/null; then
    echo "   ✓ All Python dependencies are installed"
else
    echo "   ✗ Missing Python dependencies"
    echo "   Please run: pip install -r requirements.txt"
    exit 1
fi

# Test 2: Check environment variables
echo "2. Checking environment variables..."
REQUIRED_VARS=("OPENROUTER_API_KEY" "SUPABASE_DB_HOST" "SUPABASE_DB_USER" "SUPABASE_DB_PASSWORD")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        if [[ -f ".env" ]]; then
            # Try to load from .env file
            export $(grep -v '^#' .env | xargs)
        fi
    fi
    
    if [[ -z "${!var}" ]]; then
        MISSING_VARS+=("$var")
    fi
done

if [[ ${#MISSING_VARS[@]} -eq 0 ]]; then
    echo "   ✓ All required environment variables are set"
else
    echo "   ✗ Missing environment variables: ${MISSING_VARS[*]}"
    echo "   Please check your .env file"
    exit 1
fi

# Test 3: Test database connection
echo "3. Testing database connection..."
if $PYTHON_CMD -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_DB_HOST'),
        port=os.getenv('SUPABASE_DB_PORT', '5432'),
        database=os.getenv('SUPABASE_DB_NAME', 'postgres'),
        user=os.getenv('SUPABASE_DB_USER'),
        password=os.getenv('SUPABASE_DB_PASSWORD')
    )
    conn.close()
    print('   ✓ Database connection successful')
except Exception as e:
    print(f'   ✗ Database connection failed: {e}')
    exit(1)
" 2>/dev/null; then
    echo ""
else
    echo "   ✗ Database connection test failed"
    exit 1
fi

# Test 4: Test OpenRouter API connection
echo "4. Testing OpenRouter API connection..."
if $PYTHON_CMD -c "
import os
import sys
sys.path.append('.')
from openrouter_client import OpenRouterClient
try:
    client = OpenRouterClient(
        api_key=os.getenv('OPENROUTER_API_KEY', ''),
        primary_model=os.getenv('OPENROUTER_PRIMARY_MODEL', 'qwen/qwen-2.5-72b-instruct:free'),
        fallback_model=os.getenv('OPENROUTER_FALLBACK_MODEL', 'deepseek/deepseek-v3.1:free'),
        api_url=os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
    )
    response = client.call_api([
        {'role': 'user', 'content': 'Hello, this is a test.'}
    ], max_tokens=10)
    print('   ✓ OpenRouter API connection successful')
except Exception as e:
    print(f'   ✗ OpenRouter API connection failed: {e}')
    exit(1)
" 2>/dev/null; then
    echo ""
else
    echo "   ✗ OpenRouter API connection test failed"
    exit 1
fi

echo "============================"
echo "All tests passed! RAG service is ready to start."
echo "Run './start_rag_service.sh' to start the service."