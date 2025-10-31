# RAG Service Troubleshooting Guide

This guide helps diagnose and resolve common issues with the OpenRouter RAG service.

## Common Issues and Solutions

### 1. Service Won't Start

#### Symptoms
- "Module not found" errors
- Port already in use
- Permission denied errors

#### Solutions

**Module Not Found:**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**Port Already in Use:**
```bash
# Check if service is already running
lsof -i :8001

# Kill existing process
kill -9 <PID>

# Or change port in .env
echo "SERVICE_PORT=8002" >> .env
```

**Permission Denied:**
```bash
# Check file permissions
ls -la

# Fix permissions
chmod +x main.py
```

### 2. OpenRouter API Connection Issues

#### Symptoms
- "Authentication failed" errors
- "Model not found" errors
- Timeout errors
- Rate limit errors

#### Solutions

**Authentication Failed:**
```bash
# Verify API key in .env
cat .env | grep OPENROUTER_API_KEY

# Test API key
curl -X POST https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

**Model Not Found:**
```bash
# Check model names in .env
cat .env | grep OPENROUTER

# Verify model availability
curl -X GET https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

**Timeout Errors:**
```bash
# Increase timeout in openrouter_client.py
# Default timeout is 30 seconds
# Consider increasing for complex queries
```

**Rate Limit Errors:**
```bash
# Implement retry logic with exponential backoff
# Check OpenRouter dashboard for rate limits
# Consider caching frequent responses
```

### 3. Database Connection Issues

#### Symptoms
- "Connection refused" errors
- "Authentication failed" for database
- "Table not found" errors
- Slow query performance

#### Solutions

**Connection Refused:**
```bash
# Check database connectivity
telnet $SUPABASE_DB_HOST $SUPABASE_DB_PORT

# Verify credentials
echo $SUPABASE_DB_USER
echo $SUPABASE_DB_PASSWORD
```

**Authentication Failed:**
```bash
# Test database connection
psql -h $SUPABASE_DB_HOST -p $SUPABASE_DB_PORT -U $SUPABASE_DB_USER -d $SUPABASE_DB_NAME

# Reset credentials if needed
# Update .env file with correct values
```

**Table Not Found:**
```bash
# Check database schema
psql -h $SUPABASE_DB_HOST -p $SUPABASE_DB_PORT -U $SUPABASE_DB_USER -d $SUPABASE_DB_NAME -c "\dt"

# Run database migrations if needed
# Check Laravel migration status
php artisan migrate:status
```

**Slow Performance:**
```bash
# Add database indexes
# Check query execution plans
# Optimize knowledge sync queries
```

### 4. Laravel Integration Issues

#### Symptoms
- "Connection refused" to RAG service
- Empty or error responses
- Sync not triggering
- CORS errors

#### Solutions

**Connection Refused:**
```bash
# Check if RAG service is running
curl http://localhost:8001/health

# Verify RAG_SERVICE_URL in Laravel .env
cat .env | grep RAG_SERVICE_URL

# Check firewall settings
```

**Empty/Error Responses:**
```bash
# Check Laravel logs
tail -f storage/logs/laravel.log

# Check RAG service logs
tail -f rag_service.log

# Test endpoint directly
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "message": "Test"}'
```

**Sync Not Triggering:**
```bash
# Check Admin controllers for sync calls
grep -r "syncRagKnowledge" app/Http/Controllers/Admin/

# Verify RAG service /sync-knowledge endpoint
curl -X POST http://localhost:8001/sync-knowledge
```

**CORS Errors:**
```bash
# Check CORS configuration in main.py
# Ensure localhost origins are allowed
```

## Log Analysis

### RAG Service Logs

Check `rag_service.log` for detailed error information:

```bash
# Tail the log file
tail -f rag_service.log

# Search for specific errors
grep "ERROR" rag_service.log

# Search for specific time period
grep "2025-10-07" rag_service.log
```

### Laravel Logs

Check Laravel logs for integration issues:

```bash
# Tail Laravel logs
tail -f storage/logs/laravel.log

# Search for RAG-related errors
grep -i "rag\|chatbot" storage/logs/laravel.log
```

## Health Check Diagnostics

### Service Health Endpoint

```bash
# Check overall service health
curl http://localhost:8001/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-10-07T12:00:00Z",
  "database": "connected",
  "primary_model": "qwen/qwen-2.5-72b-instruct:free",
  "fallback_model": "deepseek/deepseek-v3.1:free"
}
```

### Model Testing

```bash
# Test OpenRouter connection
python test_rag.py

# Or manually test models
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen-2.5-72b-instruct:free",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Performance Issues

### Slow Response Times

1. **Check System Resources:**
```bash
# Monitor CPU and memory
top
htop

# Check disk I/O
iostat
```

2. **Optimize Database Queries:**
```bash
# Analyze slow queries
# Add appropriate indexes
# Optimize knowledge sync process
```

3. **Cache Frequently Used Data:**
```bash
# Implement Laravel caching
# Cache student context
# Cache common responses
```

### High Memory Usage

1. **Monitor Memory Consumption:**
```bash
# Check Python process memory
ps aux | grep python

# Use memory profiling tools
pip install memory-profiler
```

2. **Optimize Data Handling:**
```bash
# Process data in chunks
# Release unused resources
# Use generators for large datasets
```

## Data Sync Issues

### Knowledge Sync Failures

1. **Check Sync Endpoint:**
```bash
# Manual sync test
curl -X POST http://localhost:8001/sync-knowledge

# Check sync status
curl http://localhost:8001/status
```

2. **Verify Database Access:**
```bash
# Test direct database connection
psql -h $SUPABASE_DB_HOST -p $SUPABASE_DB_PORT -U $SUPABASE_DB_USER -d $SUPABASE_DB_NAME

# Check table permissions
\dt
```

### Missing Data

1. **Verify Data Existence:**
```bash
# Check if data exists in database
psql -c "SELECT COUNT(*) FROM assessments WHERE is_active = true;"

# Check sync logs for errors
grep "sync" rag_service.log
```

2. **Force Full Sync:**
```bash
# Trigger forced sync
curl -X POST http://localhost:8001/sync-knowledge \
  -H "Content-Type: application/json" \
  -d '{"force": true}'
```

## Security Issues

### API Key Compromise

1. **Rotate API Keys:**
```bash
# Generate new OpenRouter API key
# Update .env files
# Restart services
```

2. **Audit API Usage:**
```bash
# Check OpenRouter dashboard
# Monitor for unusual activity
# Set up usage alerts
```

### Unauthorized Access

1. **Check Service Accessibility:**
```bash
# Ensure service only accepts localhost connections
# Verify CORS settings
# Check firewall rules
```

2. **Review Logs for Suspicious Activity:**
```bash
# Look for unusual request patterns
# Check for unauthorized access attempts
# Monitor error logs
```

## Testing and Validation

### Automated Testing

Run the test suite to validate functionality:

```bash
# Run all tests
python test_rag.py

# Run specific tests
python -m pytest test_rag.py::test_openrouter_connection
```

### Manual Testing

1. **Basic Chat Functionality:**
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "message": "What assessments are available?",
    "student_email": "student@example.com",
    "student_name": "John Doe"
  }'
```

2. **Knowledge Sync:**
```bash
curl -X POST http://localhost:8001/sync-knowledge
```

## Recovery Procedures

### Service Restart

```bash
# Stop the service
pkill -f "python main.py"

# Start the service
python main.py
```

### Database Recovery

```bash
# Check database connectivity
# Restore from backups if needed
# Re-run sync process
```

### Configuration Recovery

```bash
# Restore .env from backup
# Verify all configuration values
# Restart services
```

## Monitoring and Alerts

### Set Up Health Checks

```bash
# Create a monitoring script
#!/bin/bash
curl -f http://localhost:8001/health || echo "RAG service down!"
```

### Log Rotation

```bash
# Set up log rotation to prevent disk space issues
# Use logrotate or similar tools
```

## Contact Support

If you're unable to resolve issues:

1. **Check Documentation**: Review all documentation files
2. **Search Issues**: Look for similar problems in issue trackers
3. **Community Support**: Reach out to relevant communities
4. **Professional Support**: Contact system administrators or developers