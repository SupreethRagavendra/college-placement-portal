# ⚡ Quick Start - Docker Deployment to Render

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub (30 seconds)
```bash
git push origin main
```

### Step 2: Set Environment Variables in Render (2 minutes)

**Go to**: https://dashboard.render.com → Your Service → Environment

**Laravel Service** (`college-placement-portal`):
```
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD=Supreeeth24#
GROQ_API_KEY=your_groq_api_key_here
```

**RAG Service** (`rag-service`):
```
DB_PASSWORD=Supreeeth24#
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Step 3: Verify Settings (1 minute)

**Laravel Service Settings:**
- Runtime: **Docker** ✅
- Health Check Path: **/healthz** ✅
- Region: **Oregon (US West)** ✅

**RAG Service Settings:**
- Runtime: **Docker** ✅
- Dockerfile Path: **./python-rag/Dockerfile** ✅
- Docker Context: **./python-rag** ✅
- Health Check Path: **/health** ✅

### Step 4: Wait for Deployment (10-15 minutes)
Watch the build logs in Render Dashboard

### Step 5: Test (1 minute)
```bash
# Test Laravel
curl https://college-placement-portals.onrender.com/healthz

# Test RAG
curl https://rag-service.onrender.com/health

# Open in browser
open https://college-placement-portals.onrender.com/
```

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ Health checks return `{"status":"healthy"}`
- ✅ Landing page loads with CSS styling
- ✅ No 404 errors in browser console
- ✅ Database connection shows "connected"

---

## 🆘 If Something Goes Wrong

### Quick Fixes:

**500 Error?**
- Check APP_KEY is set in Render
- Check DB_PASSWORD is correct

**Assets Not Loading?**
- Wait 30 seconds (cold start)
- Clear browser cache
- Check build logs for "npm run build"

**Database Connection Failed?**
- Verify DB_PORT=6543 (not 5432)
- Check DB_SSLMODE=require
- Verify DB_USERNAME=postgres.wkqbukidxmzbgwauncrl

**Need More Help?**
- Read: `TROUBLESHOOTING_DOCKER.md`
- Check: Render Dashboard → Logs tab

---

## 📚 Full Documentation

- **Complete Guide**: `DOCKER_DEPLOYMENT_GUIDE.md`
- **Troubleshooting**: `TROUBLESHOOTING_DOCKER.md`
- **Quick Reference**: `RENDER_QUICK_REFERENCE.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Summary**: `DOCKER_DEPLOYMENT_SUMMARY.md`

---

## 🎉 That's It!

Your College Placement Portal is now deployed with:
- ✅ Docker containers
- ✅ Nginx + PHP-FPM
- ✅ Python RAG service
- ✅ Auto-deployment
- ✅ Health monitoring
- ✅ Production optimization

**Main URL**: https://college-placement-portals.onrender.com
**RAG URL**: https://rag-service.onrender.com

---

**First load may take 30-60 seconds due to free tier cold start.**
