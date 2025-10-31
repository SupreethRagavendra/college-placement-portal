# 🔧 Render Environment Variables Setup

## ⚠️ CRITICAL: You MUST set these in Render Dashboard

Go to: https://dashboard.render.com → `college-placement-portal` → **Environment** tab

Click **Add Environment Variable** for each one below:

---

## 📋 Required Environment Variables

### 1. Application Settings

```
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=true
APP_URL=https://college-placement-portals.onrender.com
```

### 2. Application Key (MOST IMPORTANT!)

**Generate locally first:**
```bash
cd d:\project-mini\college-placement-portal
php artisan key:generate --show
```

**Copy the output and add to Render:**
```
APP_KEY=base64:YOUR_GENERATED_KEY_HERE
```

Example:
```
APP_KEY=base64:8T8IXwcv1CIAhAlBdzN4BCinMsQbGeEUEUqQ5kn6BSY=
```

### 3. Database Settings (Supabase)

```
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require
```

### 4. Logging Settings

```
LOG_CHANNEL=stack
LOG_LEVEL=debug
LOG_STACK=single,stderr
```

### 5. Cache & Session Settings

```
CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_CONNECTION=sync
```

### 6. Optional: RAG Chatbot (Disable for now)

```
RAG_ENABLED=false
RAG_SERVICE_URL=http://localhost:8001
```

---

## 🎯 Quick Copy-Paste (After Generating APP_KEY)

**Replace `YOUR_APP_KEY_HERE` with the key you generated:**

```
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=true
APP_URL=https://college-placement-portals.onrender.com
APP_KEY=YOUR_APP_KEY_HERE

DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require

LOG_CHANNEL=stack
LOG_LEVEL=debug
LOG_STACK=single,stderr

CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_CONNECTION=sync

RAG_ENABLED=false
```

---

## ✅ Verification Checklist

After adding all variables:

- [ ] APP_KEY is set (starts with `base64:`)
- [ ] APP_URL matches your Render URL
- [ ] DB_HOST matches your Supabase host
- [ ] DB_PASSWORD is correct
- [ ] All variables are saved (click Save button)

---

## 🚀 After Setting Variables

1. **Trigger Manual Deploy:**
   - In Render Dashboard, click **Manual Deploy** → **Deploy latest commit**

2. **Or push new commit:**
   ```bash
   git add .
   git commit -m "Update render configuration"
   git push origin main
   ```

3. **Monitor Logs:**
   - Go to Logs tab
   - Watch for successful build
   - Check for any errors

---

## 🐛 Troubleshooting

### If you see "No application encryption key"
→ APP_KEY is not set or invalid
→ Generate new key and add it

### If you see "Database connection failed"
→ Check DB_HOST, DB_PASSWORD are correct
→ Verify Supabase database is running

### If you see "Class not found"
→ Clear build cache in Render
→ Redeploy

---

**Last Updated:** 2025-10-10
