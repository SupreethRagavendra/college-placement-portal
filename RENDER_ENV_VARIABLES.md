# Render.com Environment Variables Configuration Guide

## 📋 Complete Environment Variables for Both Services

### 🟦 Laravel Application (college-placement-portal)

**Service URL:** `https://college-placement-portal-t1mt.onrender.com`

#### Required Environment Variables:

```bash
# Application
APP_NAME="College Placement Portal"
APP_ENV=production
APP_KEY=base64:BkMKrOJeUKQ39EuvLFgmKUU5KqQMLfFK/gjxEFrWemQ=
APP_DEBUG=false
APP_URL=https://college-placement-portal-t1mt.onrender.com

# Locale
APP_LOCALE=en
APP_FALLBACK_LOCALE=en

# Logging
LOG_CHANNEL=stderr
LOG_STACK=single
LOG_LEVEL=info

# Database (Supabase PostgreSQL - Using Pooler)
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=6543
DB_DATABASE=postgres
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=1cxdxcwjE6zL9Wvd
DB_SSLMODE=require

# Session
SESSION_DRIVER=database
SESSION_LIFETIME=120
SESSION_ENCRYPT=false
SESSION_DOMAIN=.onrender.com
SESSION_SECURE_COOKIE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax

# Cache
CACHE_DRIVER=file
CACHE_STORE=file

# Queue
QUEUE_CONNECTION=sync

# Mail (Gmail SMTP)
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=aromaticrootq@gmail.com
MAIL_PASSWORD=efmffwbmyrvrtdej
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=aromaticrootq@gmail.com
MAIL_FROM_NAME="College Placement Portal"

# RAG Service Connection
RAG_SERVICE_URL=https://placement-rag-service.onrender.com
RAG_SERVICE_TIMEOUT=30
RAG_ENABLED=true
RAG_AUTO_SYNC=true
RAG_CACHE_ENABLED=true
RAG_CACHE_TTL=300

# OpenRouter API
OPENROUTER_API_KEY=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
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free

# Groq API
GROQ_API_KEY=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
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024

# Security
SANCTUM_STATEFUL_DOMAINS=college-placement-portal-t1mt.onrender.com
TRUSTED_PROXIES=*

# PHP
PHP_MEMORY_LIMIT=256M
PHP_MAX_EXECUTION_TIME=60
```

---

### 🟩 Python RAG Service (placement-rag-service)

**Service URL:** `https://placement-rag-service.onrender.com`

#### Required Environment Variables:

```bash
# Service Configuration
PORT=8001
DEBUG=false

# Database (Supabase PostgreSQL - Using Pooler)
SUPABASE_DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.wkqbukidxmzbgwauncrl
SUPABASE_DB_PASSWORD=1cxdxcwjE6zL9Wvd
SUPABASE_DB_SSLMODE=require

# OpenRouter API
OPENROUTER_API_KEY=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
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free
OPENROUTER_TEMPERATURE=0.7
OPENROUTER_MAX_TOKENS=1024

# Groq API (Fallback)
GROQ_API_KEY=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
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024

# ChromaDB
CHROMA_PERSIST_DIR=./chromadb_storage
CHROMA_COLLECTION_NAME=placement_knowledge

# Laravel App URL (for CORS)
LARAVEL_APP_URL=https://college-placement-portal-t1mt.onrender.com
```

---

## 🚀 How to Add Environment Variables in Render

### For Laravel Service:
1. Go to: https://dashboard.render.com/web/YOUR_LARAVEL_SERVICE_ID/env
2. Click **"Edit"** button
3. Click **"Add"** → **"New variable"** for each variable
4. OR Click **"Add"** → **"From .env"** and paste all variables at once

### For RAG Service:
1. Go to: https://dashboard.render.com/web/srv-d427o0je5dus73bgil30/env
2. Click **"Edit"** button  
3. Click **"Add"** → **"New variable"** for each variable
4. OR Click **"Add"** → **"From .env"** and paste all variables at once

### 📝 Quick Copy for RAG Service (.env format):

Copy this entire block and paste into "From .env" dialog:

```
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free
GROQ_API_KEY=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
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024
CHROMA_PERSIST_DIR=./chromadb_storage
CHROMA_COLLECTION_NAME=placement_knowledge
LARAVEL_APP_URL=https://college-placement-portal-t1mt.onrender.com
DEBUG=false
PORT=8001
SUPABASE_DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.wkqbukidxmzbgwauncrl
SUPABASE_DB_SSLMODE=require
```

---

## ✅ Current Status

### Laravel Service:
- ✅ Deployed and LIVE
- ✅ Environment variables configured
- ✅ URL: https://college-placement-portal-t1mt.onrender.com

### RAG Service:
- ✅ Deployment started
- ⚠️ Environment variables: 3/14 added
  - ✅ OPENROUTER_API_KEY
  - ✅ OPENROUTER_API_URL  
  - ✅ SUPABASE_DB_PASSWORD
  - ⏳ Need to add: 11 more variables
- ✅ URL: https://placement-rag-service.onrender.com

---

## 🔍 Important Notes

1. **Database Port:** Use `6543` (Supabase pooler) for Render, NOT `5432`
2. **SSL Mode:** Use `require` for production, NOT `prefer`
3. **Username Format:** Use `postgres.wkqbukidxmzbgwauncrl` (with project ID)
4. **ChromaDB Path:** Use `./chromadb_storage` (relative path works in Render)
5. **CORS:** Ensure `LARAVEL_APP_URL` matches your Laravel service URL exactly

---

## 🎯 Next Steps

1. ✅ Add remaining environment variables to RAG service
2. ⏳ Wait for RAG service build to complete
3. ✅ Verify both services are running
4. ✅ Test RAG chatbot integration



