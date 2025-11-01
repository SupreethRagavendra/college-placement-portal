# Deployment Split Guide

## Project Size Reduction Strategy

Your 8GB project has been split for free hosting deployment on Render.com.

### Size Breakdown

| Component | Original | After Split | Deployment Target |
|-----------|----------|-------------|-------------------|
| **Laravel Main App** | ~3GB | ~500MB-1GB | Render.com Web Service |
| **Python RAG Service** | ~1GB | ~200MB | Render.com Web Service |
| **ChromaDB Vector DB** | ~4GB | Excluded | Rebuilt at runtime |
| **Documentation** | ~100MB | Excluded | GitHub only |
| **TOTAL** | ~8GB | ~700MB-1.2GB | Deployed |

---

## Files/Folders Excluded from Laravel Deployment

### 1. Python RAG Service (deployed separately)
```
python-rag/                    # Entire RAG service
python-rag-groq-backup/       # Backup of RAG service
```

### 2. ChromaDB Storage (large binary files ~4GB)
```
chromadb_storage/             # Vector database storage
*.bin                         # Binary data files
*.sqlite3                     # SQLite database files
*.db                          # Database files
*.db-shm                      # Shared memory files
*.db-wal                      # Write-ahead log files
```

### 3. Documentation Files
```
docs/                         # Contains large PDFs and Word docs
  - College_Placement_Portal_Report.docx
  - Project Doc.pdf
  - ACADEMIC_PROJECT_DOCUMENTATION.md
  - CHAPTER_2_SYSTEM_ANALYSIS.md

*.md                          # All markdown docs except README.md
*.pdf
*.docx
*.doc
```

### 4. Development & Deployment Scripts
```
*.bat                         # Windows batch files
*.sh                          # Shell scripts
deploy-to-render.sh
render-build.sh
render-diagnose.sh
setup-render-env.sh
oracle-setup.sh
deploy-email-function.sh
clear-cache.bat
optimize-production.bat
etc.
```

### 5. Configuration & Analysis Files
```
*.txt                         # Text analysis files
email-test-output.txt
verification-result.txt
env-timeout-fix.txt
RENDER_FINAL_FIX.txt
```

### 6. IDE & OS Files
```
.vscode/
.idea/
.DS_Store
Thumbs.db
*.swp
*.swo
```

### 7. Cache & Temporary Files
```
storage/logs/*
storage/framework/cache/*
storage/framework/sessions/*
storage/framework/views/*
bootstrap/cache/*
__pycache__/
*.cache
```

### 8. Docker Files
```
docker-compose.yml            # Not needed for Render
docker/                       # Docker configs
supervisor/
php.ini
php.ini.production
```

### 9. Supabase Functions
```
supabase/                     # Separate deployment
```

### 10. Various Documentation MD Files
All the `*_FIX*.md`, `*_SUMMARY.md`, `*_GUIDE.md`, etc. files in root.

---

## Step 1: Prepare GitHub Repository

### 1.1 Initialize Git (if not already done)
```bash
cd "C:\Users\supree\OneDrive\Documents\college-placement-portals-main (1)\college-placement-portals-main"

# Initialize git
git init

# Add .gitignore if not exists
git add .gitignore
```

### 1.2 Commit All Files to Git
```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: College Placement Portal with Laravel + Python RAG"
```

### 1.3 Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `college-placement-portal`
3. **DO NOT** initialize with README, .gitignore, or license (we already have them)

### 1.4 Push to GitHub
```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/college-placement-portal.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Expected push size:** ~500MB-1GB (after exclusions)

---

## Step 2: Deploy Laravel App to Render.com

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

### 2.2 Create Web Service

1. **New → Web Service**
2. **Connect GitHub** and select your repo
3. **Configure Service:**
   - **Name:** `college-placement-portal`
   - **Region:** `Oregon (US West)`
   - **Branch:** `main`
   - **Root Directory:** Leave empty (root)
   - **Runtime:** `Docker`
   - **Dockerfile Path:** `Dockerfile`
   - **Instance Type:** `Free`

4. **Environment Variables:**

```bash
# Application
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=false
APP_URL=https://YOUR_SERVICE.onrender.com
APP_KEY=base64:GENERATE_NEW_KEY

# Database (Supabase PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
DB_SSLMODE=require

# Cache & Session
CACHE_DRIVER=file
SESSION_DRIVER=database
SESSION_LIFETIME=120

# Security
SANCTUM_STATEFUL_DOMAINS=YOUR_SERVICE.onrender.com
TRUSTED_PROXIES=*

# PHP
PHP_MEMORY_LIMIT=256M
PHP_MAX_EXECUTION_TIME=60

# RAG Service (we'll add this after deploying RAG)
RAG_SERVICE_URL=http://rag-service.onrender.com
RAG_ENABLED=true
RAG_SERVICE_TIMEOUT=30

# Groq API (if using)
GROQ_API_KEY=YOUR_GROQ_KEY
GROQ_MODEL=llama-3.3-70b-versatile
```

5. **Advanced Settings:**
   - Build Command: (leave empty, handled by Dockerfile)
   - Start Command: (handled by Dockerfile)
   - Health Check Path: `/healthz`

6. **Deploy!**

---

## Step 3: Deploy Python RAG Service to Render.com

### 3.1 Create Second Web Service

1. **New → Web Service** (in same Render dashboard)
2. **Connect GitHub** (same repo)
3. **Configure Service:**
   - **Name:** `rag-service`
   - **Region:** `Oregon (US West)` (same as Laravel)
   - **Branch:** `main`
   - **Root Directory:** `python-rag`
   - **Runtime:** `Docker`
   - **Dockerfile Path:** `python-rag/Dockerfile`
   - **Instance Type:** `Free`

4. **Environment Variables:**

```bash
# Service Configuration
PORT=8001
DEBUG=false

# Database Connection (Supabase)
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
DB_SSLMODE=require

# OpenRouter API
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
OPENROUTER_TEMPERATURE=0.7
OPENROUTER_MAX_TOKENS=1024

# ChromaDB Configuration (persists in ephemeral storage on free tier)
CHROMA_PERSIST_DIR=./chromadb_storage
CHROMA_COLLECTION_NAME=placement_knowledge
```

5. **Advanced Settings:**
   - Build Command: (leave empty)
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 8001 --workers 1`
   - Health Check Path: `/health`

6. **Deploy!**

---

## Step 4: Connect Services

### 4.1 Update Laravel RAG URL

After RAG service deploys, update Laravel environment:

1. Go to **Render Dashboard → Laravel Service → Environment**
2. Update:
   ```bash
   RAG_SERVICE_URL=https://rag-service-YOUR_ID.onrender.com
   ```
3. **Save Changes** (triggers redeploy)

### 4.2 Rebuild ChromaDB

The ChromaDB vector database will be empty on first deploy. Initialize it:

1. SSH into RAG service (if available) or use Render Shell
2. Run initialization:
   ```bash
   python init_knowledge.py
   python init_vector_db.py
   ```

Or create a one-time script to initialize on first deploy.

---

## Step 5: Verify Deployment

### 5.1 Test Laravel App
```bash
curl https://YOUR_SERVICE.onrender.com
```

### 5.2 Test RAG Service
```bash
curl https://rag-service.onrender.com/health
```

### 5.3 Test Integration
```bash
curl -X POST https://YOUR_SERVICE.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello, how can you help me with placements?"}'
```

---

## Step 6: Monitor & Maintain

### 6.1 Render Free Tier Limitations
- **Service spins down** after 15 minutes of inactivity
- **First request** takes ~30-50 seconds (cold start)
- **512MB RAM** limit per service
- **No persistent storage** (ChromaDB will be rebuilt on each deploy)

### 6.2 ChromaDB Persistence Solution

Since free tier has no persistent storage:

**Option A: Rebuild on Deploy**
- Add initialization script to Dockerfile
- Vector DB rebuilds automatically

**Option B: Use Supabase Vector (better for production)**
- Migrate to pgvector extension in Supabase
- Persistent and scalable

**Option C: Upgrade to Paid Tier**
- $7/month for persistent disk storage

### 6.3 Performance Optimization

1. **Enable build caching** in Render settings
2. **Use health checks** to keep services warm
3. **Monitor logs** for errors
4. **Set up alerts** for downtime

---

## Quick Reference

### Laravel Service URLs
- **Main URL:** `https://college-placement-portal.onrender.com`
- **Health Check:** `https://college-placement-portal.onrender.com/healthz`

### RAG Service URLs
- **Main URL:** `https://rag-service.onrender.com`
- **Health Check:** `https://rag-service.onrender.com/health`
- **API:** `https://rag-service.onrender.com/api/chat`

### Render Dashboard
- https://dashboard.render.com

### GitHub Repository
- https://github.com/YOUR_USERNAME/college-placement-portal

---

## Troubleshooting

### Issue: Build fails due to size
**Solution:** Check `.dockerignore` includes all excluded files

### Issue: RAG service can't connect to database
**Solution:** Verify Supabase credentials and SSL mode

### Issue: ChromaDB empty after deploy
**Solution:** Run initialization scripts or add to startup

### Issue: Services timing out
**Solution:** Check health check endpoints, increase timeout settings

### Issue: Memory limit exceeded
**Solution:** Reduce workers, optimize queries, upgrade tier

---

## Cost Summary

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Laravel Web Service | Free | $7/month |
| RAG Web Service | Free | $7/month |
| PostgreSQL (Supabase) | Free (500MB) | $25/month |
| **Total** | **$0/month** | **$18.50/month** |

Free tier is perfect for development and light production use!

---

## Next Steps

1. ✅ Create `.slugignore` - Done
2. ✅ Update `.dockerignore` - Done
3. ⏭️ Push to GitHub
4. ⏭️ Deploy Laravel to Render
5. ⏭️ Deploy RAG to Render
6. ⏭️ Connect services
7. ⏭️ Test & monitor




