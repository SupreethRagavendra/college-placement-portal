# RAG Chatbot Deployment Guide

## Prerequisites
- Python 3.8+ installed
- Laravel application running
- PostgreSQL database configured
- OpenRouter API key

## Step 1: Install Python Dependencies

```bash
cd python-rag
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

Create or update `.env` file in `python-rag/` directory:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

# Database Configuration (Supabase/PostgreSQL)
SUPABASE_DB_HOST=your_db_host
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=your_db_name
SUPABASE_DB_USER=your_db_user
SUPABASE_DB_PASSWORD=your_db_password

# Service Configuration
SERVICE_PORT=8001
HOST=0.0.0.0
DEBUG=False
```

## Step 3: Run Laravel Migrations

```bash
# From Laravel root directory
php artisan migrate
```

This creates:
- `chatbot_conversations` table (for conversation history)
- `chatbot_analytics` table (for tracking metrics)

## Step 4: Initialize Vector Database

```bash
cd python-rag
python init_vector_db.py
```

Expected output:
```
============================================================
Initializing Vector Database
============================================================
Found 3 markdown files to process
Processing faqs.md...
Processing placement_guidelines.md...
Processing study_tips.md...

Extracted XX sections from all files
Adding documents to vector database...
============================================================
✓ Vector Database Initialized Successfully
============================================================
```

## Step 5: Start RAG Service

```bash
# Start the service
python main.py

# Or use the batch file (Windows)
start_openrouter_rag.bat
```

Service will start on `http://localhost:8001`

## Step 6: Verify Service Health

Open browser or use curl:
```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "primary_model": "qwen/qwen-2.5-72b-instruct:free",
  "fallback_model": "deepseek/deepseek-v3.1:free"
}
```

## Step 7: Run Tests

```bash
cd python-rag
python test_rag_system.py
```

Tests will verify:
- ✓ Health check
- ✓ Knowledge base retrieval (RAG)
- ✓ Conversation memory
- ✓ Response caching
- ✓ Personalized queries
- ✓ Query classification

## Step 8: Clear Laravel Cache

```bash
php artisan cache:clear
php artisan config:clear
```

## Step 9: Test in Browser

1. Navigate to: `http://localhost:8000`
2. Login as student
3. Open chatbot widget
4. Try test queries:
   - "How do I start an assessment?"
   - "Show available assessments"
   - "Tips for aptitude improvement"

## Verification Checklist

- [ ] Python dependencies installed
- [ ] Environment variables configured
- [ ] Migrations run successfully
- [ ] Vector database initialized
- [ ] RAG service running on port 8001
- [ ] Health check returns "healthy"
- [ ] Test suite passes
- [ ] Laravel cache cleared
- [ ] Chatbot responds in browser
- [ ] Conversation memory works (follow-up questions)
- [ ] Cache hit rate > 0% after repeated queries

## Monitoring

### Check Service Logs
```bash
tail -f python-rag/rag_service.log
```

### Check Laravel Logs
```bash
tail -f storage/logs/laravel.log
```

### Check Analytics
Query the `chatbot_analytics` table:
```sql
SELECT 
    query_type,
    COUNT(*) as count,
    AVG(response_time_ms) as avg_time,
    SUM(CASE WHEN from_cache THEN 1 ELSE 0 END) as cached_count
FROM chatbot_analytics
WHERE created_at >= NOW() - INTERVAL '1 day'
GROUP BY query_type;
```

## Performance Metrics

### Expected Performance
- **Response Time (uncached):** 2-4 seconds
- **Response Time (cached):** 0.3-0.7 seconds
- **Cache Hit Rate:** 40-60% (after warm-up)
- **Database Query Time:** 50-200ms
- **Vector Search Time:** 100-300ms

### Cost Estimation (per 1000 queries)
- **Qwen 2.5 72B Instruct:** FREE! 🎉
- **DeepSeek V3.1:** FREE! 🎉
- **With 50% cache hit:** Still FREE!
- **Monthly (10,000 queries):** $0.00 (100% FREE!)

## Troubleshooting

### RAG Service Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
netstat -ano | findstr :8001
```

### Vector Database Errors
```bash
# Clear and reinitialize
rm -rf chroma_db/
python init_vector_db.py
```

### Cache Not Working
```bash
# Laravel cache
php artisan cache:clear

# Python cache is in-memory (restart service)
```

### Database Connection Issues
```bash
# Test connection
python debug_db.py

# Check credentials in .env
```

## Production Deployment

### For Production:
1. Set `DEBUG=False` in `.env`
2. Use process manager (systemd, supervisor, pm2)
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Enable monitoring (Prometheus, Grafana)
6. Configure log rotation
7. Set up automated backups

### Systemd Service Example
Create `/etc/systemd/system/rag-chatbot.service`:
```ini
[Unit]
Description=RAG Chatbot Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/college-portal/python-rag
Environment="PATH=/var/www/college-portal/python-rag/venv/bin"
ExecStart=/var/www/college-portal/python-rag/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rag-chatbot
sudo systemctl start rag-chatbot
sudo systemctl status rag-chatbot
```

## Maintenance

### Daily
- Check error logs
- Monitor response times
- Verify cache hit rate

### Weekly
- Review analytics data
- Identify common failed queries
- Update knowledge base if needed

### Monthly
- Clean up old analytics (keep 90 days)
- Update dependencies
- Review API costs
- Optimize prompts based on usage

## Support

For issues or questions:
1. Check logs first
2. Run test suite
3. Review this guide
4. Check OpenRouter status
5. Verify database connectivity

## Next Steps

After deployment:
1. Add more knowledge base documents
2. Fine-tune query classification
3. Optimize cache TTL based on usage
4. Create admin dashboard for analytics
5. Implement A/B testing for prompts
6. Add user feedback collection
7. Set up automated monitoring alerts

