# 🔧 Fix for Render 500 Internal Server Error

## Quick Fix Steps

### 1. Set Environment Variables in Render Dashboard

Go to [Render Dashboard](https://dashboard.render.com) → Your Service → Environment Tab

Add these **REQUIRED** variables:

```
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=Supreeeth24#
```

### 2. Deploy the Fixed Code

```bash
git add .
git commit -m "Fix: Add TrustProxies middleware and improve health checks for Render"
git push origin main
```

### 3. Monitor Deployment

1. Watch the build logs in Render Dashboard
2. Once deployed, check: https://college-placement-portals.onrender.com/health.php
3. This will show you exactly what's working and what's not

## What Was Fixed

1. **Added TrustProxies Middleware** - Required for Render's proxy setup
2. **Improved APP_KEY handling** in build script
3. **Added health check endpoint** at `/health.php` for debugging
4. **Updated health check path** in render.yaml

## Debugging Steps

### Check Health Status
Visit: https://college-placement-portals.onrender.com/health.php

This will show:
- PHP version status
- Missing extensions
- Missing environment variables
- Storage directory issues
- Asset build status

### Check Database Connection
Visit: https://college-placement-portals.onrender.com/test-db

### View Laravel Logs
In Render Dashboard → Logs tab, look for Laravel error messages

## Common Issues and Solutions

### Issue: "No application encryption key has been specified"
**Solution**: Make sure APP_KEY is set in Render environment variables

### Issue: "SQLSTATE[08006] could not connect to server"
**Solution**: Verify all DB_* environment variables are set correctly

### Issue: "The stream or file storage/logs/laravel.log could not be opened"
**Solution**: The build script should create these directories, but check build logs

### Issue: Page loads but no CSS/JS
**Solution**: Check if `npm run build` completed successfully in build logs

## Emergency Fallback

If the site still shows 500 error after all fixes:

1. **Enable detailed error logging** by setting in Render:
   ```
   APP_DEBUG=true
   LOG_LEVEL=debug
   ```

2. **Check the raw error** by visiting the site - it should show the actual error

3. **Once fixed**, disable debug mode:
   ```
   APP_DEBUG=false
   LOG_LEVEL=error
   ```

## Verification Checklist

- [ ] APP_KEY is set in Render environment
- [ ] All DB_* variables are set correctly
- [ ] Build completes without errors
- [ ] /health.php shows all checks as "ok"
- [ ] /test-db shows successful connection
- [ ] Site loads without 500 error
- [ ] Login page appears with proper styling

## Support

If you still see errors after following these steps:
1. Check /health.php for specific issues
2. Review the Render logs for error messages
3. The TrustProxies middleware should handle Render's proxy configuration
4. Make sure the database credentials are exactly as shown (including the # in password)
