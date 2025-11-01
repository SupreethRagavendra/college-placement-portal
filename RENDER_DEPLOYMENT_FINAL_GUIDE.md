# 🚀 COMPLETE RENDER DEPLOYMENT GUIDE
## Deploy Your College Placement Portal with RAG Chatbot

---

## 📋 OVERVIEW

This guide will help you deploy your **Laravel + Python RAG Service** to Render.com **FREE tier**.

**What will be deployed:**
1. **Laravel Application** (Main portal)
2. **Python FastAPI RAG Service** (Chatbot backend)

**Estimated Time:** 15-20 minutes

---

## ✅ PRE-DEPLOYMENT CHECKLIST

Before starting, ensure:
- ✅ Your code is pushed to GitHub: `https://github.com/SupreethRagavendra/college-placement-portal-ragchatbot.git`
- ✅ You have a Render.com account (we'll create one if needed)
- ✅ Your Supabase database is accessible
- ✅ All environment variables are ready

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### **STEP 1: PUSH CODE TO GITHUB**

Open PowerShell/Terminal in your project directory:

```powershell
# Navigate to project directory
cd "C:\Users\supree\OneDrive\Documents\college-placement-portals-main (1)\college-placement-portals-main"

# Check git status
git status

# Add all files
git add .

# Commit changes
git commit -m "Configure for Render deployment with RAG service"

# Push to GitHub
git push origin main
```

**Wait for:** "Successfully pushed to GitHub" message

---

### **STEP 2: CREATE/LOGIN TO RENDER ACCOUNT**

1. **Open Chrome browser** and go to: **https://render.com**
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your repositories
5. You'll be redirected to Render Dashboard

**Once you're logged in, type "done" and I'll proceed with the next steps!**

---

### **STEP 3: DEPLOY USING RENDER BLUEPRINT (EASIEST METHOD)**

After you say "done", I'll guide you through:

#### **Option A: Using Blueprint (Recommended)**

1. In Render Dashboard, click **"New +"** (top right)
2. Select **"Blueprint"**
3. Connect your GitHub repository: `college-placement-portal-ragchatbot`
4. Render will automatically detect `render.yaml` and configure both services
5. Review the configuration and click **"Apply"**

#### **Option B: Manual Deployment (If Blueprint doesn't work)**

I'll provide detailed manual steps after you confirm login.

---

### **STEP 4: SET ENVIRONMENT VARIABLES**

After services are created, you'll need to set these environment variables manually in Render Dashboard:

#### **For Laravel Service (`college-placement-portal`):**

1. Go to your Laravel service
2. Click **"Environment"** tab
3. Add/Update these variables:

```
APP_URL=https://your-service-name.onrender.com
SANCTUM_STATEFUL_DOMAINS=your-service-name.onrender.com
```

**Note:** Replace `your-service-name` with your actual Render service URL.

#### **For RAG Service (`placement-rag-service`):**

1. Go to your RAG service
2. Click **"Environment"** tab
3. Add/Update:

```
LARAVEL_APP_URL=https://your-laravel-service-name.onrender.com
```

---

### **STEP 5: WAIT FOR DEPLOYMENT**

Both services will build and deploy automatically:

1. **Laravel Service:** ~5-10 minutes (Docker build)
2. **RAG Service:** ~3-5 minutes (Python dependencies)

**Monitor the build logs** in Render Dashboard for any errors.

---

### **STEP 6: VERIFY DEPLOYMENT**

#### **Check Laravel Service:**
- Visit: `https://your-service-name.onrender.com`
- Should see your login page

#### **Check RAG Service:**
- Visit: `https://your-rag-service-name.onrender.com/health`
- Should see: `{"status": "healthy", ...}`

---

## 🔧 TROUBLESHOOTING

### **Build Fails:**

1. **Laravel Build Issues:**
   - Check Dockerfile exists
   - Verify `composer.json` is valid
   - Check build logs for specific errors

2. **RAG Service Build Issues:**
   - Verify `python-rag/requirements.txt` exists
   - Check Python version (should be 3.8+)
   - Review build logs

### **Services Won't Connect:**

1. **Check Environment Variables:**
   - Verify `RAG_SERVICE_URL` is set correctly
   - Verify `LARAVEL_APP_URL` matches actual URL

2. **Check CORS:**
   - RAG service CORS should include Laravel URL
   - Update `python-rag/main.py` if needed

### **Database Connection Issues:**

1. **Verify Supabase credentials:**
   - Check `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`
   - Ensure database allows connections from Render IPs

2. **Check SSL Mode:**
   - Should be `prefer` or `require`

---

## 📝 POST-DEPLOYMENT CHECKLIST

After successful deployment:

- [ ] Laravel app loads at `https://your-app.onrender.com`
- [ ] RAG service health check passes
- [ ] Can login to admin panel
- [ ] Chatbot responds to queries
- [ ] Email verification works
- [ ] Database queries work

---

## 🌐 YOUR LIVE URLS

After deployment, you'll have:

1. **Main Application:** `https://college-placement-portal.onrender.com`
2. **RAG Service:** `https://placement-rag-service.onrender.com`

**Note:** Render free tier URLs may take 30-60 seconds to wake up if idle.

---

## 💡 IMPORTANT NOTES

1. **Free Tier Limitations:**
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - 750 hours/month free (enough for 24/7 single service)

2. **Database:**
   - Using your existing Supabase database
   - No changes needed to database structure

3. **Environment Variables:**
   - Most are already in `render.yaml`
   - Only `APP_URL` and `LARAVEL_APP_URL` need manual update after deployment

4. **Updates:**
   - Push to GitHub → Render auto-deploys
   - No manual deployment needed

---

## 🆘 NEED HELP?

If you encounter issues:
1. Check Render build logs
2. Check Render runtime logs
3. Verify environment variables
4. Test database connection separately

---

**Ready to start?** 

1. **First, push your code to GitHub** (Step 1)
2. **Then login to Render** (Step 2)
3. **Say "done" when logged in**, and I'll guide you through the rest!

