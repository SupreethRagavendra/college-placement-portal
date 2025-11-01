# 🚀 RENDER QUICK START GUIDE

## ✅ What's Been Configured

1. **render.yaml** - Updated with all your environment variables
2. **Python RAG Service** - Configured to use Render's PORT variable
3. **Docker Configuration** - Updated to work with Render's dynamic ports
4. **Deployment Guide** - Complete step-by-step instructions created

---

## 🎯 NEXT STEPS (Do This Now)

### Step 1: Push to GitHub

```powershell
cd "C:\Users\supree\OneDrive\Documents\college-placement-portals-main (1)\college-placement-portals-main"
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Login to Render

1. Open Chrome browser
2. Go to: **https://render.com**
3. Click **"Get Started"** or **"Sign In"**
4. Choose **"Sign in with GitHub"**
5. Authorize Render

### Step 3: Say "done" when logged in

Once you're logged into Render, type **"done"** and I'll guide you through deploying both services!

---

## 📋 What Will Be Deployed

1. **Laravel Application** (Main Portal)
   - URL: `https://college-placement-portal.onrender.com`
   - Uses Docker runtime
   - Free tier

2. **Python RAG Service** (Chatbot Backend)
   - URL: `https://placement-rag-service.onrender.com`
   - Uses Python runtime
   - Free tier

---

## ⚙️ Environment Variables Already Set

✅ All your environment variables are configured in `render.yaml`:
- Database credentials (Supabase)
- Email settings (Gmail SMTP)
- OpenRouter API keys
- Groq API keys
- RAG service configuration

**Only 2 variables need manual update after deployment:**
- `APP_URL` (Laravel service)
- `LARAVEL_APP_URL` (RAG service)

---

## 🆘 Quick Troubleshooting

**Build fails?**
- Check Render build logs
- Verify GitHub repo is connected
- Ensure `render.yaml` is in root directory

**Services won't connect?**
- Wait for both services to finish deploying
- Check environment variables match actual URLs
- Verify CORS settings in RAG service

---

**Ready?** Push to GitHub, login to Render, then say **"done"**! 🚀

