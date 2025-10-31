#!/bin/bash

# Start RAG Service Script
# This script starts the OpenRouter RAG service

# Check if we're on Windows (Git Bash) or Linux/Mac
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows with Git Bash
    echo "Starting RAG service on Windows..."
    python main.py
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Starting RAG service on macOS..."
    python3 main.py
else
    # Linux
    echo "Starting RAG service on Linux..."
    python3 main.py
fi