# 🔧 Docker Deployment Troubleshooting Guide

## 🚨 Common Issues and Solutions

---

## 1. Build Failures

### Issue: "npm ERR! code ELIFECYCLE"
**Cause**: Node build failed during Vite compilation

**Solution**:
```bash
# Check package.json scripts
cat package.json | grep "build"

# Verify Node version in Dockerfile
# Should be: nodejs npm (Alpine package)

# Test locally
npm ci
npm run build
```

### Issue: "composer install failed"
**Cause**: Composer dependencies conflict or missing

**Solution**:
```bash
# Update composer.lock
composer update --lock

# Clear composer cache
composer clear-cache

# Try with different flags
composer install --no-dev --no-scripts --prefer-dist
```

### Issue: "Docker build timeout"
**Cause**: Build taking too long (>15 minutes)

**Solution**:
- Optimize Dockerfile layer caching
- Use `.dockerignore` to exclude unnecessary files
- Consider using multi-stage builds

---

## 2. Runtime Errors

### Issue: "502 Bad Gateway"
**Symptoms**: Nginx returns 502 error

**Diagnosis**:
```bash
# Check if PHP-FPM is running
ps aux | grep php-fpm

# Check PHP-FPM logs
tail -f /var/log/php-fpm.log

# Test PHP-FPM socket
curl http://127.0.0.1:9000
```

**Solution**:
```bash
# Restart PHP-FPM via supervisor
supervisorctl restart php-fpm

# Check PHP-FPM configuration
cat /usr/local/etc/php-fpm.d/www.conf
```

### Issue: "Connection refused on port 8000"
**Symptoms**: Health check fails, container restarts

**Diagnosis**:
```bash
# Check if Nginx is listening
netstat -tlnp | grep 8000

# Check Nginx error logs
tail -f /var/log/nginx/error.log

# Test Nginx configuration
nginx -t
```

**Solution**:
```bash
# Verify Nginx config
cat /etc/nginx/http.d/default.conf

# Restart Nginx
supervisorctl restart nginx
```

### Issue: "Permission denied" errors
**Symptoms**: Laravel can't write to storage

**Diagnosis**:
```bash
# Check storage permissions
ls -la storage/
ls -la bootstrap/cache/

# Check ownership
ls -la storage/ | grep www-data
```

**Solution**:
```bash
# Fix permissions (already in start.sh)
chown -R www-data:www-data storage bootstrap/cache
chmod -R 775 storage bootstrap/cache
```

---

## 3. Database Connection Issues

### Issue: "SQLSTATE[08006] could not connect to server"
**Symptoms**: Health check shows database disconnected

**Diagnosis**:
```bash
# Test database connection
php artisan tinker
>>> DB::connection()->getPdo();

# Check environment variables
echo $DB_HOST
echo $DB_PORT
echo $DB_DATABASE
```

**Solutions**:

**A. Wrong Port**
```bash
# Use connection pooler port
DB_PORT=6543  # NOT 5432
```

**B. Wrong Username Format**
```bash
# Include project reference
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
```

**C. SSL Mode**
```bash
# Supabase requires SSL
DB_SSLMODE=require
```

**D. Test Connection Manually**
```bash
# Using psql (if available)
psql "postgresql://postgres.wkqbukidxmzbgwauncrl:PASSWORD@db.wkqbukidxmzbgwauncrl.supabase.co:6543/postgres?sslmode=require"
```

### Issue: "Too many connections"
**Cause**: Connection pool exhausted

**Solution**:
```bash
# Use connection pooler (port 6543)
DB_PORT=6543

# Reduce max connections in config/database.php
'max_connections' => 10
```

---

## 4. Asset Loading Issues

### Issue: "404 Not Found" for CSS/JS files
**Symptoms**: 
- Page loads but no styling
- Console shows: `GET /build/assets/app-xxx.js 404`

**Diagnosis**:
```bash
# Check if build directory exists
ls -la public/build/

# Check Vite manifest
cat public/build/manifest.json

# Check build logs
grep "vite build" /var/log/supervisor/supervisord.log
```

**Solutions**:

**A. Vite Build Failed**
```bash
# Rebuild assets
npm run build

# Check for errors
npm run build 2>&1 | tee build.log
```

**B. Wrong Asset Path**
```bash
# Verify APP_URL in .env
APP_URL=https://college-placement-portals.onrender.com

# Clear config cache
php artisan config:clear
php artisan config:cache
```

**C. Missing Manifest**
```bash
# Ensure Vite built successfully
ls -la public/build/manifest.json

# Check vite.config.js
cat vite.config.js
```

---

## 5. Session/CSRF Issues

### Issue: "CSRF token mismatch"
**Symptoms**: Forms fail with 419 error

**Diagnosis**:
```bash
# Check session configuration
php artisan tinker
>>> config('session.driver')
>>> config('session.domain')
```

**Solutions**:

**A. Trust Proxies**
```bash
# Verify in bootstrap/app.php
$middleware->trustProxies(at: '*');
```

**B. Session Driver**
```bash
# Use cookie sessions (not database)
SESSION_DRIVER=cookie
SESSION_SECURE_COOKIE=true
```

**C. Clear Sessions**
```bash
# Clear session storage
rm -rf storage/framework/sessions/*
php artisan cache:clear
```

### Issue: "Session store not set on request"
**Cause**: Session middleware not loaded

**Solution**:
```bash
# Verify middleware in bootstrap/app.php
# Session middleware should be in web group

# Clear config
php artisan config:clear
```

---

## 6. Memory/Performance Issues

### Issue: "Allowed memory size exhausted"
**Symptoms**: 500 error, memory limit exceeded

**Solution**:
```bash
# Increase memory limit in php.ini
memory_limit = 256M

# Or in Dockerfile
RUN echo "memory_limit = 512M" > /usr/local/etc/php/conf.d/memory.ini
```

### Issue: "Maximum execution time exceeded"
**Cause**: Long-running requests

**Solution**:
```bash
# Increase timeouts in php.ini
max_execution_time = 300

# And in Nginx
fastcgi_read_timeout 300;
```

---

## 7. Migration Issues

### Issue: "Migration failed"
**Symptoms**: Database tables not created

**Diagnosis**:
```bash
# Check migration status
php artisan migrate:status

# View migration errors
php artisan migrate --force 2>&1
```

**Solutions**:

**A. Fresh Migration**
```bash
# Reset and re-run (CAUTION: deletes data)
php artisan migrate:fresh --force
```

**B. Specific Migration**
```bash
# Run one migration
php artisan migrate --path=/database/migrations/xxxx_create_users_table.php --force
```

**C. Rollback and Retry**
```bash
php artisan migrate:rollback --force
php artisan migrate --force
```

---

## 8. Container Restart Loop

### Issue: Container keeps restarting
**Symptoms**: Service shows "Starting" but never becomes healthy

**Diagnosis**:
```bash
# Check Render logs
# Look for:
# - Startup script errors
# - Health check failures
# - Port binding issues
```

**Common Causes**:

**A. Health Check Failing**
```bash
# Test health endpoint locally
curl http://localhost:8000/healthz

# Check if route exists
php artisan route:list | grep healthz
```

**B. Port Not Listening**
```bash
# Verify Nginx is on port 8000
netstat -tlnp | grep 8000

# Check Nginx config
grep "listen" /etc/nginx/http.d/default.conf
```

**C. Startup Script Failed**
```bash
# Check start.sh logs
tail -f /var/log/supervisor/supervisord.log

# Test start.sh manually
bash -x /start.sh
```

---

## 9. RAG Service Issues

### Issue: "RAG service not responding"
**Symptoms**: Laravel can't connect to RAG service

**Diagnosis**:
```bash
# Test RAG health endpoint
curl https://rag-service.onrender.com/health

# Check RAG service logs in Render
```

**Solutions**:

**A. Service Not Started**
```bash
# Verify uvicorn is running
ps aux | grep uvicorn

# Check Python logs
tail -f /app/logs/rag_service.log
```

**B. Wrong URL**
```bash
# Verify RAG_SERVICE_URL in Laravel
echo $RAG_SERVICE_URL

# Should be: https://rag-service.onrender.com
```

**C. CORS Issues**
```bash
# Update CORS in main.py
allow_origins=[
    "https://college-placement-portals.onrender.com",
    "*"  # For testing only
]
```

---

## 10. Environment Variable Issues

### Issue: "Environment variable not set"
**Symptoms**: Config values are null or default

**Diagnosis**:
```bash
# Check if variable is set
printenv | grep APP_KEY

# Check Laravel config
php artisan tinker
>>> env('APP_KEY')
>>> config('app.key')
```

**Solutions**:

**A. Not Set in Render**
```bash
# Go to Render Dashboard → Environment
# Add missing variables
# Save and redeploy
```

**B. Config Cached**
```bash
# Clear config cache
php artisan config:clear

# Rebuild cache
php artisan config:cache
```

**C. Wrong Format**
```bash
# APP_KEY must start with base64:
APP_KEY=base64:xxxxx...

# No quotes needed in Render
APP_KEY=base64:xxxxx  # ✅ Correct
APP_KEY="base64:xxxxx"  # ❌ Wrong
```

---

## 🔍 Debugging Commands

### Check Service Status
```bash
# Supervisor status
supervisorctl status

# Process list
ps aux | grep -E "nginx|php-fpm"

# Port listening
netstat -tlnp
```

### View Logs
```bash
# Nginx access log
tail -f /var/log/nginx/access.log

# Nginx error log
tail -f /var/log/nginx/error.log

# PHP-FPM log
tail -f /var/log/php-fpm.log

# Laravel log
tail -f storage/logs/laravel.log

# Supervisor log
tail -f /var/log/supervisor/supervisord.log
```

### Test Components
```bash
# Test Nginx config
nginx -t

# Test PHP
php -v
php -m

# Test database
php artisan db:show

# Test cache
php artisan cache:clear
php artisan config:clear
```

### Laravel Diagnostics
```bash
# Application info
php artisan about

# Route list
php artisan route:list

# Config values
php artisan tinker
>>> config('database.connections.pgsql')
```

---

## 📊 Health Check Debugging

### Test Health Endpoint
```bash
# From outside
curl -i https://college-placement-portals.onrender.com/healthz

# From inside container
curl -i http://localhost:8000/healthz

# Expected response
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "database": "connected"
}
```

### If Health Check Fails
```bash
# Check route exists
php artisan route:list | grep healthz

# Test database connection
php artisan tinker
>>> DB::connection()->getPdo();

# Check logs
tail -f storage/logs/laravel.log
```

---

## 🆘 Emergency Recovery

### Complete Reset
```bash
# 1. Clear all caches
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear

# 2. Rebuild caches
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 3. Fix permissions
chown -R www-data:www-data storage bootstrap/cache
chmod -R 775 storage bootstrap/cache

# 4. Restart services
supervisorctl restart all
```

### Rollback Deployment
```bash
# In Render Dashboard:
# 1. Go to service
# 2. Click "Events" tab
# 3. Find last successful deploy
# 4. Click "Rollback to this version"
```

---

## 📞 Getting Help

If issues persist:

1. **Check Render Status**: https://status.render.com
2. **Review Logs**: Render Dashboard → Logs tab
3. **Test Locally**: Build Docker image locally first
4. **GitHub Issues**: Check repository issues
5. **Render Support**: support@render.com

---

**Last Updated**: 2025-10-11
