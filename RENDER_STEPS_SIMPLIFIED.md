# 🎯 RENDER DEPLOYMENT - STEP BY STEP GUIDE

After you successfully push to GitHub, follow these exact steps:

---

## 📍 STEP 1: SIGN UP FOR RENDER

1. Open: **https://render.com**
2. Click **"Get Started"** (top right)
3. Choose **"Sign in with GitHub"**
4. Enter your GitHub credentials
5. Click **"Authorize Render"** when prompted
6. You'll see Render Dashboard

---

## 📍 STEP 2: DEPLOY LARAVEL APPLICATION

### 2.1 Create New Web Service

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your repositories
4. Find **"TEST-DEP-COLLEGE"** and click **"Connect"**

### 2.2 Configure Laravel Service

Fill in these exact settings:

```yaml
Name:                 college-placement-portal
Region:               Oregon (US West)
Branch:               main
Root Directory:       (leave BLANK)
Runtime:              Docker
Instance Type:        Free
```

**Build Command:**
```bash
composer install --no-dev --optimize-autoloader && npm install && npm run build && php artisan config:cache && php artisan route:cache && php artisan view:cache
```

**Start Command:**
```bash
php artisan migrate --force && php artisan serve --host=0.0.0.0 --port=$PORT
```

### 2.3 Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

**Click "Add Environment Variable"** and add these ONE BY ONE:

```
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
APP_URL=https://college-placement-portal.onrender.com

DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=6543
DB_DATABASE=postgres
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require

SESSION_DRIVER=cookie
SESSION_SECURE_COOKIE=true
SESSION_LIFETIME=120
CACHE_DRIVER=file
QUEUE_CONNECTION=sync

LOG_CHANNEL=stderr
LOG_LEVEL=info

TRUSTED_PROXIES=*

GROQ_API_KEY=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
```

> **Note**: We'll add `RAG_SERVICE_URL` after deploying the RAG service

### 2.4 Deploy

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 10-20 minutes for build
4. Watch logs for errors
5. When you see **"Your service is live 🎉"**, copy the URL

**Your Laravel URL**: `https://college-placement-portal.onrender.com`

---

## 📍 STEP 3: DEPLOY RAG SERVICE

### 3.1 Create Second Web Service

1. Go back to Render Dashboard (click "Render" logo top left)
2. Click **"New +"** → **"Web Service"**
3. Find **"TEST-DEP-COLLEGE"** again and click **"Connect"**

### 3.2 Configure RAG Service

Fill in these settings:

```yaml
Name:                 placement-rag-service
Region:               Oregon (US West) - SAME as Laravel
Branch:               main
Root Directory:       python-rag          ← IMPORTANT!
Runtime:              Python 3
Instance Type:        Free
```

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3.3 Add RAG Environment Variables

Click **"Advanced"** → **"Environment Variables"**

Add these ONE BY ONE:

```
PORT=8001
DEBUG=false
PYTHONUNBUFFERED=1
ENVIRONMENT=production

SUPABASE_DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.wkqbukidxmzbgwauncrl
SUPABASE_DB_PASSWORD=Supreeeth24#

OPENROUTER_API_KEY=your_openrouter_key_if_you_have_one
OPENROUTER_PRIMARY_MODEL=meta-llama/llama-3.1-70b-instruct
OPENROUTER_FALLBACK_MODEL=meta-llama/llama-3.1-8b-instruct
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

GROQ_API_KEY=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

LARAVEL_APP_URL=https://college-placement-portal.onrender.com

CHROMA_PERSIST_DIRECTORY=/tmp/chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

> **CRITICAL**: Make sure **Root Directory** is set to `python-rag`!

### 3.4 Deploy RAG Service

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 5-10 minutes
4. When live, copy the URL

**Your RAG URL**: `https://placement-rag-service.onrender.com`

---

## 📍 STEP 4: CONNECT THE SERVICES

### 4.1 Add RAG URL to Laravel

1. Go to Render Dashboard
2. Click on **"college-placement-portal"** service
3. Click **"Environment"** in left sidebar
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `RAG_SERVICE_URL`
   - **Value**: `https://placement-rag-service.onrender.com`
6. Click **"Save Changes"**
7. Service will auto-redeploy (~5 min)

---

## 📍 STEP 5: VERIFY DEPLOYMENT

### Test Laravel

Open in browser:
```
https://college-placement-portal.onrender.com
```

**Expected**: You should see the homepage with styling

### Test RAG Service

Open in browser:
```
https://placement-rag-service.onrender.com/health
```

**Expected**: JSON response like:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-31T...",
  "database": "connected"
}
```

### Test Login

1. Go to Laravel URL
2. Click **Login**
3. Enter:
   - **Email**: `admin@portal.com`
   - **Password**: `Admin@123`
4. If login works → Database connected ✅

---

## ✅ SUCCESS!

Your application is now live on Render!

### 📝 Important Notes:

1. **Cold Starts**: Services sleep after 15 min inactivity (free tier)
   - First request after sleep takes 30-60 seconds
   - This is normal for free tier

2. **Auto-Deploy**: Every `git push` triggers auto-deploy
   - Both services will rebuild
   - Takes ~10-15 minutes

3. **Logs**: View logs in Render Dashboard
   - Click service → "Logs" tab
   - Real-time logs for debugging

4. **Custom Domain**: Can add later in Settings

---

## 🆘 TROUBLESHOOTING

### Issue: Build Timeout

**Solution**: Check `.slugignore` excludes large files

### Issue: Database Connection Failed

**Solution**: Verify `DB_PORT=6543` (not 5432)

### Issue: Assets Not Loading

**Solution**: Check `npm run build` completed in logs

### Issue: RAG Service Won't Start

**Solution**: Verify **Root Directory = python-rag**

---

## 📞 NEED HELP?

Check the detailed guide: `RENDER_DEPLOYMENT_COMPLETE_GUIDE.md`

---

**Created**: October 31, 2025  
**Version**: 1.0.0

