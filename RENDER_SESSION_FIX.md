# Render Session Fix - Login/Register 500 Error

## Problem
Login and registration were failing with 500 errors on Render but working locally. This was caused by:

1. **Session Driver Mismatch**: `render.yaml` specified `SESSION_DRIVER=file` which has permission issues in Docker containers
2. **Config Caching**: The startup script was caching configuration, locking in wrong session settings
3. **Missing Session Domain**: Session cookies weren't properly configured for Render's subdomain
4. **Duplicate CSRF Tokens**: Login form had redundant CSRF token fields
5. **No Error Handling**: Session initialization failures caused silent 500 errors

## Solution Applied

### 1. Updated Session Configuration (`render.yaml`)
```yaml
- key: SESSION_DRIVER
  value: cookie  # Changed from 'file' to 'cookie'
- key: SESSION_DOMAIN
  value: .onrender.com  # Added for Render compatibility
```

**Why cookie driver?**
- More reliable in containerized/stateless environments
- No file system permissions issues
- Works better behind proxies (like Render's load balancer)
- Handles horizontal scaling better

### 2. Fixed Startup Script (`docker/start.sh`)
- **Removed `config:cache`** - This was locking session settings
- **Added early permission setup** - Before migrations
- **Added session functionality test** - To catch issues early
- Only cache routes and views (config remains dynamic)

### 3. Updated Session Config (`config/session.php`)
```php
'domain' => env('SESSION_DOMAIN', null),
'secure' => env('SESSION_SECURE_COOKIE', env('APP_ENV') === 'production'),
```

### 4. Added Session Error Handling (`SupabaseAuthController.php`)
- Tests session before login/register
- Provides clear error messages
- Logs session failures for debugging

### 5. Fixed Login Form (`resources/views/auth/login.blade.php`)
- Removed duplicate CSRF token field
- `@csrf` directive is sufficient

## Deployment Steps

### On Render Dashboard:

1. **Update Environment Variables** (if not using render.yaml):
   ```
   SESSION_DRIVER=cookie
   SESSION_DOMAIN=.onrender.com
   SESSION_SECURE_COOKIE=true
   SESSION_HTTP_ONLY=true
   SESSION_SAME_SITE=lax
   ```

2. **Clear Application Cache**:
   - Go to your service > Shell
   - Run: `php artisan config:clear`
   - Run: `php artisan cache:clear`

3. **Deploy the Changes**:
   - Commit and push these changes
   - Render will automatically rebuild and deploy
   - OR manually trigger deploy from Render dashboard

4. **Verify Deployment**:
   - Check build logs for `✅ Session test passed`
   - Test login at: `https://your-app.onrender.com/login`
   - Test registration at: `https://your-app.onrender.com/register`

### Testing Locally:

```bash
# Test with production-like settings
SESSION_DRIVER=cookie php artisan serve

# Or test with Docker
docker-compose up --build
```

## Verification Checklist

After deployment, verify:
- [ ] Build logs show "✅ Session test passed"
- [ ] Login page loads without errors
- [ ] Register page loads without errors
- [ ] Can submit login form (even with wrong credentials)
- [ ] Can submit register form
- [ ] CSRF token errors are gone
- [ ] Session cookies are being set (check browser DevTools)

## Troubleshooting

### Still getting 500 errors?

1. **Check Render Logs**:
   ```bash
   # In Render shell or logs
   tail -f storage/logs/laravel.log
   ```

2. **Check for APP_KEY**:
   ```bash
   # Should be set in Render env vars
   echo $APP_KEY
   ```

3. **Check Database Connection**:
   ```bash
   php artisan migrate:status
   ```

4. **Clear Browser Cookies**:
   - Clear all cookies for `.onrender.com`
   - Try in incognito/private mode

### Session cookies not being set?

1. **Verify HTTPS**:
   - Render serves over HTTPS by default
   - `SESSION_SECURE_COOKIE=true` requires HTTPS

2. **Check Proxy Headers**:
   - TrustProxies middleware is already set to `*`
   - Render's X-Forwarded-* headers are trusted

3. **Check Session Domain**:
   - For `app.onrender.com` use `.onrender.com`
   - For custom domain `example.com` use `.example.com`

### CSRF token mismatch?

1. **Clear config cache**:
   ```bash
   php artisan config:clear
   ```

2. **Regenerate APP_KEY** (only if really needed):
   ```bash
   php artisan key:generate --show
   # Update in Render env vars
   ```

## Performance Notes

- **Cookie sessions** have a 4KB size limit
- For large session data, consider Redis (requires paid plan)
- Current setup works for standard auth flows

## Files Modified

1. `render.yaml` - Session configuration
2. `docker/start.sh` - Startup script fixes
3. `config/session.php` - Session config defaults
4. `app/Http/Controllers/SupabaseAuthController.php` - Error handling
5. `resources/views/auth/login.blade.php` - Removed duplicate CSRF

## Rollback Plan

If issues persist:

1. **Revert to file sessions** (with proper permissions):
   ```yaml
   SESSION_DRIVER=file
   ```
   And ensure storage directory has 775 permissions

2. **Or use database sessions**:
   ```bash
   php artisan session:table
   php artisan migrate
   ```
   ```yaml
   SESSION_DRIVER=database
   ```

## Support

If problems continue:
- Check Laravel logs: `storage/logs/laravel.log`
- Check Render logs: Dashboard > Logs
- Enable debug mode temporarily: `APP_DEBUG=true` (remember to disable after!)

