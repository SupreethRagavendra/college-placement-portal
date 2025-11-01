# 🚀 RENDER DEPLOYMENT - QUICK START GUIDE

## ✅ PREPARATION COMPLETE!

Your code is optimized and pushed to GitHub. Chrome browser is opening Render.com.

---

## 📌 DEPLOYMENT STEPS (Follow in Browser)

### STEP 1: Sign In to Render (2 minutes)

1. **In the browser tab that just opened:**
   - Click **"Sign In"**
   - Choose **"Sign in with GitHub"**
   - Authorize Render to access your repositories
   - You'll be redirected to Render Dashboard

---

### STEP 2: Deploy Laravel Service (15-20 minutes)

#### A. Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if you don't see your repository
4. Find: **college-placement-portal**
5. Click **"Connect"**

#### B. Configure Service
**Basic Settings:**
- **Name**: `college-placement-portal`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Root Directory**: [LEAVE EMPTY]
- **Runtime**: `Docker`
- **Instance Type**: `Free`

#### C. Add Environment Variables
Click **"Add Environment Variable"** and add these **3 CRITICAL** variables:

```
APP_KEY = base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD = Supreeeth24#
GROQ_API_KEY = [YOUR_GROQ_API_KEY]
```

**Note**: All other variables are auto-configured from `render.yaml`!

#### D. Deploy!
1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 10-15 minutes
4. Watch build logs
5. Service should turn **GREEN** ✅

**Expected URL**: `https://college-placement-portal.onrender.com`

---

### STEP 3: Deploy RAG Service (8-12 minutes)

#### A. Create Second Service
1. Go back to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **SAME repository**: `college-placement-portal`
4. Click **"Connect"**

#### B. Configure RAG Service
**Basic Settings:**
- **Name**: `placement-rag-service`
- **Region**: `Oregon (US West)` [SAME as Laravel!]
- **Branch**: `main`
- **Root Directory**: `python-rag` ← **CRITICAL!**
- **Runtime**: `Python 3`
- **Instance Type**: `Free`

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### C. Add Environment Variables
Click **"Add Environment Variable"** and add these **3 CRITICAL** variables:

```
SUPABASE_DB_PASSWORD = Supreeeth24#
OPENROUTER_API_KEY = [YOUR_OPENROUTER_KEY]
GROQ_API_KEY = [YOUR_GROQ_KEY]
```

**Note**: All other variables are auto-configured from `render.yaml`!

#### D. Deploy!
1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 8-12 minutes
4. Watch build logs
5. Service should turn **GREEN** ✅

**Expected URL**: `https://placement-rag-service.onrender.com`

---

## 🔑 WHERE TO GET API KEYS

### Groq API Key (FREE - Required)
1. Go to: https://console.groq.com
2. Sign up/Login
3. Click **"API Keys"** in sidebar
4. Click **"Create API Key"**
5. Copy the key
6. Paste in both services

### OpenRouter API Key (FREE tier - Required for RAG)
1. Go to: https://openrouter.ai
2. Sign up/Login
3. Click **"Keys"** in menu
4. Click **"Create Key"**
5. Copy the key
6. Paste in RAG service only

---

## ✅ VERIFICATION (After Both Services Deploy)

### Test Laravel:
Open in browser: `https://college-placement-portal.onrender.com`
- Should see styled homepage ✅
- Login: **admin@portal.com** / **Admin@123** ✅
- Admin dashboard loads ✅

### Test RAG Service:
Open in browser: `https://placement-rag-service.onrender.com/health`
- Should return JSON: `{"status": "healthy"}` ✅
- Try docs: `https://placement-rag-service.onrender.com/docs` ✅

### Test Integration:
1. Login to Laravel portal
2. Find chatbot widget
3. Send message: "What is this portal about?"
4. Should get AI response ✅

---

## 🎯 YOUR LIVE URLS

### Main Application:
**URL**: https://college-placement-portal.onrender.com
**Admin**: admin@portal.com / Admin@123

### RAG API:
**URL**: https://placement-rag-service.onrender.com
**Health**: /health
**Docs**: /docs

### Database:
**Provider**: Supabase PostgreSQL (already configured)

---

## ⚠️ IMPORTANT NOTES

1. **First Request Slow**: Services sleep after 15 min. First request takes 30-60 seconds.
2. **Root Directory**: CRITICAL for RAG service - must be `python-rag`
3. **API Keys**: Without them, services won't work properly
4. **Watch Build Logs**: If build fails, read logs for specific error
5. **Free Tier**: 750 hours/month per service (plenty for testing!)

---

## 🐛 QUICK TROUBLESHOOTING

**Build Fails**:
- Check build logs for specific error
- Most common: Missing environment variables
- Solution: Add the 3 required variables

**500 Error**:
- Missing APP_KEY
- Database connection failed
- Check logs in Render dashboard

**RAG Service Won't Start**:
- Check Root Directory = `python-rag`
- Verify requirements.txt exists
- Check Python logs

**Services Can't Talk**:
- Verify both are GREEN/running
- Check CORS in python-rag/main.py
- Restart both services

---

## 🎉 YOU'RE DONE!

Total time: **25-35 minutes**
Total cost: **$0/month**

Your College Placement Portal with AI Chatbot is now LIVE! 🚀

Share the URL with your stakeholders and start testing!

---

**Need help?** Check `RENDER_DEPLOYMENT_FINAL.md` for detailed troubleshooting.



