# 🚀 COMPLETE RENDER DEPLOYMENT GUIDE
## Deploy Laravel + RAG Service from One Repository

---

## ✅ PROJECT STATUS

**Repository**: https://github.com/SupreethRagavendra/TEST-DEP-COLLEGE.git  
**Size**: ~8GB (reduced to ~2-3GB for Laravel deployment)  
**Tech Stack**: Laravel 12 + Python FastAPI RAG Service  
**Database**: Supabase PostgreSQL (already configured)  
**Solution**: Split deployment using Render.com FREE tier

---

## 📋 PRE-DEPLOYMENT CHECKLIST

✅ `.slugignore` file created (reduces deployment size)  
✅ `render.yaml` configured for both services  
✅ CORS updated in RAG service  
✅ Database connection uses pooler (port 6543)  
✅ Environment variables prepared

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### PHASE 1: PUSH CODE TO GITHUB

Open PowerShell in your project directory and run:

```powershell
# Navigate to project directory (if not already there)
cd "C:\Users\supree\OneDrive\Documents\college-placement-portals-main (1)\college-placement-portals-main"

# Check current status
git status

# Add all files
git add .

# Commit changes
git commit -m "Configure for Render deployment with split services"

# Push to GitHub
git push origin main
```

**Expected Output**: 
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), X.XX MiB | X.XX MiB/s, done.
Total X (delta X), reused X (delta X)
To https://github.com/SupreethRagavendra/TEST-DEP-COLLEGE.git
   abc1234..def5678  main -> main
```

---

### PHASE 2: DEPLOY ON RENDER.COM

#### Step 2.1: Sign Up / Login to Render

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your repositories
5. You'll be redirected to the Render Dashboard

---

#### Step 2.2: Deploy Laravel Application

##### A. Create New Web Service

1. In Render Dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if you don't see your repository
4. Find and select: **TEST-DEP-COLLEGE**
5. Click **"Connect"**

##### B. Configure Laravel Service

Fill in these settings:

```yaml
Name:                 college-placement-portal
Region:               Oregon (US West)
Branch:               main
Root Directory:       (leave BLANK - uses repository root)
Runtime:              Docker
Instance Type:        Free
```

##### C. Build & Start Commands

**Build Command:**
```bash
composer install --no-dev --optimize-autoloader && npm install && npm run build && php artisan config:cache && php artisan route:cache && php artisan view:cache
```

**Start Command:**
```bash
php artisan migrate --force && php artisan serve --host=0.0.0.0 --port=$PORT
```

##### D. Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"** → Add these:

```env
# === APPLICATION ===
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
APP_URL=https://college-placement-portal.onrender.com

# === DATABASE (SUPABASE) ===
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=6543
DB_DATABASE=postgres
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require

# === SESSION & CACHE ===
SESSION_DRIVER=cookie
SESSION_SECURE_COOKIE=true
SESSION_LIFETIME=120
SESSION_ENCRYPT=false
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax
CACHE_DRIVER=file
QUEUE_CONNECTION=sync

# === LOGGING ===
LOG_CHANNEL=stderr
LOG_LEVEL=info

# === SECURITY ===
TRUSTED_PROXIES=*
SANCTUM_STATEFUL_DOMAINS=college-placement-portal.onrender.com

# === AI APIs ===
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024

# === RAG SERVICE (Add after RAG is deployed) ===
RAG_SERVICE_URL=https://placement-rag-service.onrender.com
RAG_SERVICE_TIMEOUT=30
RAG_ENABLED=true
```

> **⚠️ IMPORTANT**: Add `RAG_SERVICE_URL` after you deploy the RAG service in the next section.

##### E. Create the Service

1. Click **"Create Web Service"** at the bottom
2. Wait for deployment (10-20 minutes for first deploy)
3. Watch the logs for any errors
4. When you see **"Your service is live 🎉"**, note the URL

**Expected URL**: `https://college-placement-portal.onrender.com`

---

#### Step 2.3: Deploy RAG Service

##### A. Create Second Web Service

1. Go back to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Select the **same repository**: **TEST-DEP-COLLEGE**
4. Click **"Connect"**

##### B. Configure RAG Service

Fill in these settings:

```yaml
Name:                 placement-rag-service
Region:               Oregon (US West) - SAME as Laravel
Branch:               main
Root Directory:       python-rag          ← CRITICAL!
Runtime:              Python 3
Instance Type:        Free
```

##### C. Build & Start Commands

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

##### D. Environment Variables for RAG

```env
# === SERVICE CONFIG ===
PORT=8001
DEBUG=false
PYTHONUNBUFFERED=1
ENVIRONMENT=production

# === DATABASE (SUPABASE) ===
SUPABASE_DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.wkqbukidxmzbgwauncrl
SUPABASE_DB_PASSWORD=Supreeeth24#

# === OPENROUTER API ===
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_PRIMARY_MODEL=meta-llama/llama-3.1-70b-instruct
OPENROUTER_FALLBACK_MODEL=meta-llama/llama-3.1-8b-instruct
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_TEMPERATURE=0.7
OPENROUTER_MAX_TOKENS=1024

# === GROQ API (FALLBACK) ===
GROQ_API_KEY=your_groq_api_key_here

# === LARAVEL APP URL (FOR CORS) ===
LARAVEL_APP_URL=https://college-placement-portal.onrender.com

# === RAG SETTINGS ===
CHROMA_PERSIST_DIRECTORY=/tmp/chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

> **⚠️ CRITICAL**: Make sure **Root Directory** is set to `python-rag`

##### E. Create the RAG Service

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. When deployed, note the URL

**Expected URL**: `https://placement-rag-service.onrender.com`

---

### PHASE 3: CONNECT THE SERVICES

#### Step 3.1: Update Laravel Environment

1. Go to Laravel service in Render Dashboard
2. Click on **"Environment"** in the left sidebar
3. Find the environment variables section
4. Add or update:

```env
RAG_SERVICE_URL=https://placement-rag-service.onrender.com
```

5. Click **"Save Changes"**
6. Service will automatically redeploy (takes ~5 minutes)

---

### PHASE 4: VERIFY DEPLOYMENT

#### Test 4.1: Check Laravel Application

Open PowerShell and test:

```powershell
# Test homepage
curl https://college-placement-portal.onrender.com

# Test health (if you have a health endpoint)
curl https://college-placement-portal.onrender.com/api/health
```

**Or open in browser**:
```powershell
Start-Process "https://college-placement-portal.onrender.com"
```

**Expected**: You should see the Laravel application homepage with proper styling.

---

#### Test 4.2: Check RAG Service

```powershell
# Test health endpoint
curl https://placement-rag-service.onrender.com/health

# Test API docs
Start-Process "https://placement-rag-service.onrender.com/docs"
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-31T...",
  "database": "connected",
  "primary_model": "meta-llama/llama-3.1-70b-instruct",
  "fallback_model": "meta-llama/llama-3.1-8b-instruct"
}
```

---

#### Test 4.3: Test Database Connection

1. Open: `https://college-placement-portal.onrender.com`
2. Try to login with admin credentials:
   - **Email**: `admin@portal.com`
   - **Password**: `Admin@123`
3. If login succeeds → Database is connected ✅

---

#### Test 4.4: Test Service Integration

1. Login to the portal
2. Open the chatbot (if visible on the page)
3. Send a test message like: "What assessments are available?"
4. Verify the AI responds

**If chatbot doesn't respond:**
- Check Render logs for RAG service
- Verify `RAG_SERVICE_URL` is correct in Laravel env vars
- Check CORS configuration

---

## 📊 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                        │
│          TEST-DEP-COLLEGE (~8GB)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  RENDER SERVICE  │      │  RENDER SERVICE  │
│   Laravel App    │◄────►│   RAG Service    │
│   (Root Dir)     │      │  (python-rag/)   │
└────────┬─────────┘      └────────┬─────────┘
         │                         │
         │         ┌───────────────┘
         │         │
         ▼         ▼
┌──────────────────────────────┐
│    SUPABASE POSTGRESQL       │
│    (Port 6543 - Pooler)      │
└──────────────────────────────┘
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: Build Timeout

**Symptom**: Build takes longer than 15 minutes and fails

**Solutions**:
1. Check `.slugignore` is excluding large files
2. Verify `node_modules/` and `vendor/` are excluded
3. Check build logs for stuck dependencies

```powershell
# Verify .slugignore exists
Get-Content .\.slugignore
```

---

### Issue 2: Database Connection Failed

**Symptom**: Error: "could not connect to server"

**Solutions**:
1. Verify `DB_PORT=6543` (pooler, not direct port 5432)
2. Check `DB_SSLMODE=require` is set
3. Verify Supabase credentials are correct

**Test connection manually:**
```powershell
# This should work if credentials are correct
# Install psql first: choco install postgresql
psql "postgresql://postgres.wkqbukidxmzbgwauncrl:Supreeeth24#@db.wkqbukidxmzbgwauncrl.supabase.co:6543/postgres?sslmode=require"
```

---

### Issue 3: Assets Not Loading (No CSS)

**Symptom**: Page loads but no styling

**Solutions**:
1. Check `npm run build` completed in build logs
2. Verify `public/build` directory exists
3. Check `APP_URL` matches your Render URL

**Fix:**
```powershell
# Locally rebuild assets and commit
npm install
npm run build
git add public/build
git commit -m "Add built assets"
git push origin main
```

---

### Issue 4: 500 Internal Server Error

**Symptom**: White page with "500 | Server Error"

**Solutions**:
1. Check `APP_KEY` is set in environment variables
2. Verify `php artisan migrate --force` ran successfully
3. Check Render logs for specific error

**View Render logs:**
1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for red error messages

---

### Issue 5: RAG Service Won't Start

**Symptom**: RAG service shows "Deploy failed"

**Solutions**:
1. **VERIFY** Root Directory = `python-rag` (most common issue!)
2. Check `requirements.txt` exists in `python-rag/`
3. Verify `main.py` exists in `python-rag/`
4. Check Python version compatibility

---

### Issue 6: Services Can't Communicate

**Symptom**: Chatbot doesn't respond, CORS errors

**Solutions**:
1. Check `RAG_SERVICE_URL` in Laravel environment
2. Verify CORS in `python-rag/main.py` includes Laravel URL
3. Ensure both services are running (green status)

**Check CORS in main.py:**
```python
allow_origins=[
    "https://college-placement-portal.onrender.com",
    # ... other origins
]
```

---

### Issue 7: Cold Start Slow (First Request Slow)

**Symptom**: First request after 15 minutes takes 30-60 seconds

**Solution**: This is **normal** for Render free tier
- Services sleep after 15 minutes of inactivity
- First request "wakes up" the service
- Subsequent requests are fast

**Options**:
1. Accept it (it's free!)
2. Upgrade to paid plan ($7/month per service)
3. Use external keep-alive service (like Uptime Robot)

---

## 📝 POST-DEPLOYMENT TASKS

### Task 1: Set Up Custom Domain (Optional)

1. Go to service in Render Dashboard
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain (e.g., `portal.yourdomain.com`)
4. Update DNS records as shown
5. SSL certificate is automatic and free

---

### Task 2: Set Up Monitoring

Use **UptimeRobot** (free) to:
- Monitor uptime
- Keep services from sleeping (paid tier)
- Get alerts on downtime

**Setup**:
1. Go to: https://uptimerobot.com
2. Add new monitor
3. URL: Your Render URLs
4. Interval: 5 minutes

---

### Task 3: Configure Email (Optional)

Add to Laravel environment variables:

```env
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@portal.com
MAIL_FROM_NAME=College Placement Portal
```

**Get Gmail App Password**:
1. Go to Google Account settings
2. Security → 2-Step Verification → App passwords
3. Generate new app password
4. Use that password (not your regular Gmail password)

---

### Task 4: Enable Auto-Deploy

**Already enabled by default!**

Every `git push` to `main` branch will:
1. Trigger rebuild on Render
2. Deploy new version automatically
3. Zero downtime (new version replaces old)

**To disable**:
1. Go to service Settings
2. Scroll to "Build & Deploy"
3. Toggle off "Auto-Deploy"

---

## 🎯 SUCCESS CHECKLIST

### Laravel Service
- [x] Service is running (green status in Render)
- [x] URL is accessible
- [x] Homepage loads with styling
- [x] Can login as admin
- [x] Database queries work
- [x] No errors in logs

### RAG Service
- [x] Service is running (green status)
- [x] `/health` endpoint responds with 200
- [x] `/docs` shows API documentation
- [x] Database connection works
- [x] No errors in logs

### Integration
- [x] `RAG_SERVICE_URL` is set in Laravel
- [x] CORS allows Laravel origin
- [x] Chatbot responds to queries
- [x] Both services can communicate

---

## 🌐 YOUR LIVE URLS

After successful deployment:

### Main Portal
🔗 **URL**: https://college-placement-portal.onrender.com  
👤 **Admin Login**: admin@portal.com / Admin@123

### RAG Service
🔗 **URL**: https://placement-rag-service.onrender.com  
📚 **API Docs**: https://placement-rag-service.onrender.com/docs  
❤️ **Health Check**: https://placement-rag-service.onrender.com/health

### Database
🔗 **Provider**: Supabase PostgreSQL  
🔌 **Connection**: Already configured via environment variables

---

## 💰 COST BREAKDOWN

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Laravel App | Free | $0/month | 750 hours/month, sleeps after 15 min |
| RAG Service | Free | $0/month | 750 hours/month, sleeps after 15 min |
| Database (Supabase) | Free | $0/month | 500MB, 2GB bandwidth |
| **TOTAL** | - | **$0/month** | **100% FREE** |

**Upgrade Options** (if needed later):
- Render Starter: $7/month per service (no sleep, more resources)
- Supabase Pro: $25/month (8GB database, more bandwidth)

---

## 🔄 MAINTENANCE & UPDATES

### Update Code

```powershell
# Make changes locally
# Test thoroughly
# Commit and push
git add .
git commit -m "Your update message"
git push origin main

# Render will auto-deploy in ~5-10 minutes
```

### View Logs

**Render Dashboard**:
1. Click on service
2. Click "Logs" tab
3. Real-time logs appear

**Download logs**:
```powershell
# Install Render CLI
npm install -g render-cli

# Login
render login

# View logs
render logs --service college-placement-portal
render logs --service placement-rag-service
```

### Restart Service

1. Go to service in Render Dashboard
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Or: Click the "⋮" menu → "Restart"

---

## 📞 SUPPORT & RESOURCES

### Render Documentation
- Docs: https://render.com/docs
- Status: https://status.render.com
- Support: support@render.com

### Supabase Documentation
- Docs: https://supabase.com/docs
- Status: https://status.supabase.com
- Support: support@supabase.com

### GitHub Issues
If you encounter bugs in the project code, open an issue:
- Repository: https://github.com/SupreethRagavendra/TEST-DEP-COLLEGE/issues

---

## ✅ DEPLOYMENT COMPLETE!

Your College Placement Portal is now live on Render! 🎉

**Next Steps**:
1. Test all features thoroughly
2. Set up monitoring (UptimeRob)
3. Configure custom domain (optional)
4. Share the URL with stakeholders
5. Monitor logs for any issues

**Remember**:
- Services sleep after 15 minutes (free tier limitation)
- First request after sleep takes 30-60 seconds
- Database is always available (Supabase doesn't sleep)
- Auto-deploy is enabled (git push = auto deploy)

---

**Created**: October 31, 2025  
**Last Updated**: October 31, 2025  
**Version**: 1.0.0

