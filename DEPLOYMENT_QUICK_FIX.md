# Quick Fix for Login/Register 500 Error on Render

## Problem
Login and Register showing 500 error on Render but working locally.

## Root Cause
Session driver was set to `file` which doesn't work reliably in Docker containers on Render due to permission and storage issues.

## Quick Fix

### Step 1: Update Render Environment Variables

Go to your Render Dashboard → Service → Environment

**Update these variables:**
```
SESSION_DRIVER=cookie
SESSION_DOMAIN=.onrender.com
```

**Ensure these are set:**
```
SESSION_SECURE_COOKIE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax
APP_ENV=production
TRUSTED_PROXIES=*
```

### Step 2: Deploy Changes

Option A - **Push code changes** (Recommended):
```bash
git add .
git commit -m "Fix: Session configuration for Render deployment"
git push origin main
```
Render will auto-deploy.

Option B - **Manual Redeploy**:
- Go to Render Dashboard
- Click "Manual Deploy" → "Clear build cache & deploy"

### Step 3: Clear Caches (After Deploy)

In Render Shell:
```bash
php artisan config:clear
php artisan cache:clear
php artisan view:clear
```

### Step 4: Test

1. Go to: `https://your-app.onrender.com/login`
2. Try logging in with: `admin@portal.com` / `Admin@123`
3. Should work now! ✅

## What Was Fixed

### Files Changed:
1. **render.yaml** - Changed SESSION_DRIVER from `file` to `cookie`
2. **docker/start.sh** - Removed config caching, added session test
3. **config/session.php** - Better defaults for production
4. **SupabaseAuthController.php** - Added session error handling
5. **login.blade.php** - Removed duplicate CSRF token

### Why Cookie Sessions?
- ✅ No file permission issues
- ✅ Works in Docker containers
- ✅ Better for stateless/containerized deployments
- ✅ Works with Render's infrastructure
- ✅ No additional services needed (Redis/DB)

## Verification

Build logs should show:
```
✅ Session test passed
✅ Laravel application ready!
```

## Still Not Working?

### 1. Check Logs
```bash
# In Render shell
tail -f storage/logs/laravel.log
```

### 2. Verify APP_KEY is Set
```bash
echo $APP_KEY
# Should show: base64:...long-string...
```

If not set:
```bash
php artisan key:generate --show
# Copy output and add to Render env vars
```

### 3. Clear Browser Cookies
- Clear all cookies for `.onrender.com`
- Try incognito/private mode

### 4. Check Database Connection
```bash
php artisan migrate:status
# Should show list of migrations
```

### 5. Enable Debug Mode (Temporarily)
In Render env vars:
```
APP_DEBUG=true
```
Then check the actual error message.
**IMPORTANT:** Set back to `false` after debugging!

## Alternative: Database Sessions

If cookie sessions still don't work (shouldn't happen, but just in case):

```bash
# In Render shell
php artisan session:table
php artisan migrate
```

Then update env var:
```
SESSION_DRIVER=database
```

## Support

If still having issues:
1. Check Render build logs for errors
2. Check `storage/logs/laravel.log`
3. Ensure all environment variables are set correctly
4. Try manual deploy with cache clear

## Files Modified (Summary)

```
✅ render.yaml - Session configuration
✅ docker/start.sh - Startup improvements
✅ config/session.php - Better defaults
✅ app/Http/Controllers/SupabaseAuthController.php - Error handling
✅ resources/views/auth/login.blade.php - Fixed CSRF
✅ bootstrap/app.php - Middleware registration
✅ app/Http/Middleware/EnsureSessionWorks.php - New (optional)
```

All changes are backward compatible with local development!

