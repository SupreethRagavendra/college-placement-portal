# 🚀 RENDER DEPLOYMENT GUIDE - READY TO DEPLOY

## ✅ PROJECT OPTIMIZED AND READY

Your College Placement Portal with RAG Chatbot is now optimized and ready for Render deployment!

**GitHub Repository**: https://github.com/SupreethRagavendra/college-placement-portal.git

---

## 📋 WHAT WAS FIXED

### ✅ Configuration Issues Resolved:
1. **render.yaml** - Fixed service name reference (rag-service → placement-rag-service)
2. **render.yaml** - Fixed APP_URL consistency (removed typo with 's')
3. **render.yaml** - Changed LOG_LEVEL from debug to info (production best practice)
4. **.slugignore** - Already optimized to exclude large files (python-rag/, chromadb_storage/, docs/)
5. **Dockerfile** - Already configured with PHP 8.2 and PostgreSQL support
6. **CORS** - Already configured in python-rag/main.py to allow Laravel URLs

---

## 🎯 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────┐
│   GitHub Repository (Single Repo)      │
│   college-placement-portal              │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────────┐    ┌──────────────┐
│  Service 1  │◄──►│  Service 2   │
│   Laravel   │    │  RAG Python  │
│   (Docker)  │    │   (Python)   │
└──────┬──────┘    └──────┬───────┘
       │                  │
       └────────┬─────────┘
                ▼
      ┌──────────────────┐
      │ Supabase Postgres│
      │   (Port 6543)    │
      └──────────────────┘
```

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Commit and Push to GitHub

Run these commands in PowerShell:

```powershell
# Navigate to project directory
cd "C:\Users\supree\OneDrive\Documents\college-placement-portals-main (1)\college-placement-portals-main"

# Check status
git status

# Add all changes
git add .

# Commit with deployment message
git commit -m "Optimized for Render deployment - ready for production"

# Push to GitHub
git push origin main
```

**Expected Output**: Changes pushed successfully to main branch

---

### STEP 2: Deploy Laravel Service on Render

#### A. Open Render Dashboard
1. Go to: https://render.com
2. Click **"Sign In"** 
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your repositories

#### B. Create Laravel Web Service
1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Find and connect: **college-placement-portal**
4. Click **"Connect"**

#### C. Configure Laravel Service

**Basic Settings:**
```
Name:                 college-placement-portal
Region:               Oregon (US West)
Branch:               main
Root Directory:       [LEAVE BLANK]
Runtime:              Docker
Instance Type:        Free
```

**Environment Variables** (Click "Add Environment Variable"):

```env
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD=Supreeeth24#
GROQ_API_KEY=[YOUR_GROQ_API_KEY_HERE]
```

**Note**: All other environment variables are already configured in render.yaml!

#### D. Deploy Laravel Service
1. Click **"Create Web Service"**
2. Wait 10-15 minutes for build
3. Watch logs for completion
4. Note the URL: `https://college-placement-portal.onrender.com`

---

### STEP 3: Deploy RAG Service on Render

#### A. Create Second Web Service
1. Go back to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **SAME repository**: college-placement-portal
4. Click **"Connect"**

#### B. Configure RAG Service

**Basic Settings:**
```
Name:                 placement-rag-service
Region:               Oregon (US West)
Branch:               main
Root Directory:       python-rag         ← CRITICAL!
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

**Environment Variables:**

```env
SUPABASE_DB_PASSWORD=Supreeeth24#
OPENROUTER_API_KEY=[YOUR_OPENROUTER_API_KEY_HERE]
GROQ_API_KEY=[YOUR_GROQ_API_KEY_HERE]
```

**Note**: All other environment variables are already configured in render.yaml!

#### C. Deploy RAG Service
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build
3. Watch logs for completion
4. Note the URL: `https://placement-rag-service.onrender.com`

---

### STEP 4: Verify Deployment

#### Test Laravel Service:
1. Open: https://college-placement-portal.onrender.com
2. Should see styled homepage
3. Login with: **admin@portal.com** / **Admin@123**
4. Check admin dashboard loads

#### Test RAG Service:
1. Open: https://placement-rag-service.onrender.com/health
2. Should return: `{"status": "healthy"}`
3. Open: https://placement-rag-service.onrender.com/docs
4. Should see FastAPI documentation

#### Test Integration:
1. Login to Laravel portal
2. Open chatbot
3. Send test message
4. Verify AI responds

---

## 🌐 YOUR LIVE URLS

After successful deployment:

### 🔗 Laravel Portal
- **URL**: https://college-placement-portal.onrender.com
- **Admin Login**: admin@portal.com / Admin@123

### 🔗 RAG Service
- **API**: https://placement-rag-service.onrender.com
- **Health**: https://placement-rag-service.onrender.com/health
- **Docs**: https://placement-rag-service.onrender.com/docs

### 🔗 Database
- **Provider**: Supabase PostgreSQL
- **Status**: Already configured and connected

---

## 🔑 REQUIRED API KEYS

You'll need to obtain these API keys:

### 1. Groq API Key (FREE)
- Visit: https://console.groq.com
- Sign up/Login
- Go to API Keys
- Create new key
- Copy and add to both services

### 2. OpenRouter API Key (FREE tier available)
- Visit: https://openrouter.ai
- Sign up/Login
- Go to Keys
- Create new key
- Copy and add to RAG service

---

## ⚠️ IMPORTANT NOTES

### Free Tier Limitations:
- Services **sleep after 15 minutes** of inactivity
- First request after sleep takes **30-60 seconds** (cold start)
- Subsequent requests are fast
- **750 hours/month** per service (more than enough)

### Database:
- Using **Supabase pooler** (port 6543) for better performance
- SSL is **required** (already configured)
- Connection string is already in render.yaml

### Service Communication:
- Services automatically discover each other via `fromService` in render.yaml
- CORS is pre-configured
- No manual URL configuration needed

---

## 🔧 TROUBLESHOOTING

### Issue: Build fails with "out of memory"
**Solution**: This is rare on free tier. If it happens:
1. Clear build cache in Render dashboard
2. Redeploy

### Issue: Database connection fails
**Solution**: 
1. Verify DB_PASSWORD is set correctly in environment variables
2. Check Supabase is not paused (free tier auto-pauses after inactivity)
3. Log into Supabase dashboard to wake it up

### Issue: Services can't communicate
**Solution**:
1. Verify both services are deployed and running (green status)
2. Check RAG_SERVICE_URL is auto-populated in Laravel environment
3. Check logs for CORS errors

### Issue: 500 Internal Server Error
**Solution**:
1. Check APP_KEY is set in Laravel environment variables
2. View logs in Render dashboard for specific error
3. Verify migrations ran successfully (check build logs)

---

## 📊 POST-DEPLOYMENT CHECKLIST

- [ ] Laravel service deployed and running (green status)
- [ ] RAG service deployed and running (green status)
- [ ] Can access Laravel homepage
- [ ] Can login as admin
- [ ] Database queries work
- [ ] RAG service /health endpoint responds
- [ ] Chatbot responds to queries
- [ ] No errors in logs

---

## 💡 NEXT STEPS AFTER DEPLOYMENT

1. **Test thoroughly**: Try all features
2. **Set up monitoring**: Use UptimeRobot (free) to monitor uptime
3. **Custom domain** (optional): Add your own domain in Render settings
4. **Email configuration** (optional): Add SMTP settings for email features
5. **Share with stakeholders**: Send them the live URLs!

---

## 📞 SUPPORT

### If you encounter issues:
1. Check Render logs (Dashboard → Service → Logs)
2. Review this guide
3. Check Render documentation: https://render.com/docs
4. Open GitHub issue in your repository

---

## ✅ DEPLOYMENT COMPLETE!

Your College Placement Portal is now ready to go live! 🎉

Follow the steps above, and you'll have your application running in about 20-30 minutes total.

**Created**: October 31, 2025
**Status**: Ready for deployment
**Cost**: $0/month (100% FREE)

---

**Good luck with your deployment! 🚀**

