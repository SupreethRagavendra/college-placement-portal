# Render.com Deployment Guide

## 🚨 Troubleshooting 500 Server Error

If you're seeing a 500 Server Error on Render, follow these steps:

### Step 1: Check Render Logs

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your service: `college-placement-portal`
3. Click on **Logs** tab
4. Look for error messages during build or runtime

### Step 2: Verify Environment Variables

**Required Environment Variables on Render:**

Go to **Environment** tab and ensure these are set:

```env
# Application
APP_NAME=College Placement Portal
APP_ENV=production
APP_DEBUG=false
APP_URL=https://college-placement-portals.onrender.com
APP_KEY=base64:... (auto-generated or manual)

# Database (Supabase)
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require

# Logging
LOG_CHANNEL=stderr
LOG_LEVEL=error

# Cache & Session
CACHE_DRIVER=file
SESSION_DRIVER=file
QUEUE_CONNECTION=sync

# Optional: RAG Service (if using)
RAG_SERVICE_URL=http://localhost:8001
RAG_ENABLED=false
```

### Step 3: Common Issues & Fixes

#### Issue 1: Missing APP_KEY
**Error:** `No application encryption key has been specified`

**Fix:**
1. In Render dashboard, go to Environment tab
2. Add environment variable:
   - Key: `APP_KEY`
   - Value: Run locally: `php artisan key:generate --show`
   - Or let Render generate it (already configured in render.yaml)

#### Issue 2: Database Connection Failed
**Error:** `SQLSTATE[08006] could not connect to server`

**Fix:**
1. Verify Supabase database is running
2. Check database credentials in Environment variables
3. Ensure `DB_SSLMODE=require` is set
4. Test connection from local machine first

#### Issue 3: Storage Permission Errors
**Error:** `The stream or file could not be opened`

**Fix:**
- The `render-build.sh` script now creates all necessary directories
- Ensure the build script runs successfully (check build logs)

#### Issue 4: Missing Dependencies
**Error:** `Class 'X' not found`

**Fix:**
1. Clear build cache in Render (Manual Deploy → Clear build cache)
2. Redeploy the application
3. Check `composer.json` has all required packages

#### Issue 5: Route Cache Issues
**Error:** `Target class [Controller] does not exist`

**Fix:**
1. In Render Shell (or locally):
   ```bash
   php artisan config:clear
   php artisan cache:clear
   php artisan route:clear
   php artisan view:clear
   ```
2. Then rebuild caches:
   ```bash
   php artisan config:cache
   php artisan route:cache
   php artisan view:cache
   ```

### Step 4: Enable Debug Mode Temporarily

**⚠️ Only for debugging, disable after fixing!**

1. In Render Environment tab, set:
   ```
   APP_DEBUG=true
   LOG_LEVEL=debug
   ```
2. Redeploy
3. Visit the site to see detailed error messages
4. **IMPORTANT:** Set back to `false` after debugging!

### Step 5: Check Build Logs

Look for these in the build logs:

✅ **Successful build indicators:**
- `✅ Build completed successfully!`
- `Caching configuration...`
- `Running database migrations...`
- All migrations ran successfully

❌ **Failed build indicators:**
- `composer install` errors
- `npm run build` errors
- Migration errors
- Permission denied errors

### Step 6: Manual Deployment Commands

If automatic deployment fails, try manual commands in Render Shell:

```bash
# 1. Navigate to app directory
cd /opt/render/project/src

# 2. Clear all caches
php artisan optimize:clear

# 3. Run migrations
php artisan migrate --force

# 4. Cache configuration
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 5. Check if app key exists
php artisan tinker
>>> config('app.key');
```

## 📋 Deployment Checklist

Before deploying to Render:

- [ ] All environment variables are set in Render dashboard
- [ ] Database credentials are correct (test locally first)
- [ ] `render-build.sh` has execute permissions (Git tracks this)
- [ ] `.gitignore` includes proper Laravel directories
- [ ] `composer.json` has all required dependencies
- [ ] `package.json` has all frontend dependencies
- [ ] Database migrations are up to date
- [ ] No hardcoded localhost URLs in code

## 🔄 Redeployment Steps

1. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Fix deployment configuration"
   git push origin main
   ```

2. **Trigger Render deployment:**
   - Render auto-deploys on git push (if connected)
   - Or use Manual Deploy button in Render dashboard

3. **Monitor deployment:**
   - Watch build logs for errors
   - Check runtime logs after deployment
   - Test the application URL

## 🐛 Advanced Debugging

### Check PHP Version
```bash
php -v
# Should be PHP 8.2 or higher
```

### Check Database Connection
```bash
php artisan tinker
>>> DB::connection()->getPdo();
>>> DB::table('users')->count();
```

### Check File Permissions
```bash
ls -la storage/
ls -la bootstrap/cache/
# Should have write permissions
```

### Check Environment Variables
```bash
php artisan tinker
>>> config('app.key');
>>> config('database.connections.pgsql.host');
```

## 📞 Getting Help

If you're still experiencing issues:

1. **Check Render Status:** https://status.render.com
2. **Review Render Docs:** https://render.com/docs/deploy-php
3. **Check Laravel Logs:** In Render Shell: `tail -f storage/logs/laravel.log`
4. **Render Support:** https://render.com/support

## 🎯 Quick Fix Commands

Run these in Render Shell if the app is deployed but not working:

```bash
# Quick fix script
cd /opt/render/project/src
php artisan optimize:clear
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

## 📝 Notes

- **Free tier limitations:** Render free tier spins down after 15 minutes of inactivity
- **First request:** May take 30-60 seconds to spin up
- **Database:** Ensure Supabase database is on a paid plan or has sufficient free tier limits
- **Logs:** Render keeps logs for 7 days on free tier

---

**Last Updated:** 2025-10-10
