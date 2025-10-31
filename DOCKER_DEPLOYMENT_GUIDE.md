# 🚀 Complete Docker Deployment Guide for Render.com

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [File Structure](#file-structure)
3. [Environment Variables](#environment-variables)
4. [Deployment Steps](#deployment-steps)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)
7. [Post-Deployment Commands](#post-deployment-commands)

---

## 🏗️ Architecture Overview

### Services Deployed:
1. **Laravel 11 Application** (Port 8000)
   - PHP 8.2-FPM + Nginx
   - Vite-built frontend assets
   - PostgreSQL (Supabase) connection
   - Cookie-based sessions

2. **Python FastAPI RAG Service** (Port 8001)
   - ChromaDB vector database
   - OpenRouter AI integration
   - Knowledge sync with Laravel database

---

## 📁 File Structure

```
college-placement-portal/
├── Dockerfile                          # Main Laravel Dockerfile
├── render.yaml                         # Render configuration for both services
├── docker/
│   ├── nginx/
│   │   ├── nginx.conf                 # Nginx main configuration
│   │   └── default.conf               # Laravel site configuration
│   ├── php/
│   │   ├── php-fpm.conf              # PHP-FPM pool configuration
│   │   └── php.ini                    # PHP settings
│   ├── supervisor/
│   │   └── supervisord.conf          # Supervisor configuration
│   └── start.sh                       # Laravel startup script
└── python-rag/
    ├── Dockerfile                     # Python RAG service Dockerfile
    ├── main.py                        # FastAPI application
    └── requirements.txt               # Python dependencies
```

---

## 🔐 Environment Variables

### Required Environment Variables in Render Dashboard

#### Laravel Service (`college-placement-portal`)

**Critical - Must Set Manually:**
```bash
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD=Supreeeth24#
GROQ_API_KEY=your_groq_api_key_here
```

**Already Configured in render.yaml:**
- `APP_NAME=College Placement Portal`
- `APP_ENV=production`
- `APP_DEBUG=false`
- `APP_URL=https://college-placement-portals.onrender.com`
- `DB_CONNECTION=pgsql`
- `DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co`
- `DB_PORT=6543` (Connection Pooler)
- `DB_DATABASE=postgres`
- `DB_USERNAME=postgres.wkqbukidxmzbgwauncrl`
- `DB_SSLMODE=require`
- `SESSION_DRIVER=cookie`
- `CACHE_DRIVER=file`
- `LOG_CHANNEL=stderr`

#### RAG Service (`rag-service`)

**Critical - Must Set Manually:**
```bash
DB_PASSWORD=Supreeeth24#
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Already Configured in render.yaml:**
- `PORT=8001`
- `DEBUG=false`
- `DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co`
- `DB_PORT=6543`
- `DB_NAME=postgres`
- `DB_USER=postgres.wkqbukidxmzbgwauncrl`
- `OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct`

---

## 🚀 Deployment Steps

### Step 1: Generate APP_KEY (If Needed)

Run locally to generate a new APP_KEY:
```bash
php artisan key:generate --show
```

Copy the output (e.g., `base64:xxxxx...`)

### Step 2: Update Render Dashboard Settings

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Select Service**: `college-placement-portal`
3. **Click "Settings" tab**
4. **Update these settings:**
   - **Runtime**: Docker
   - **Region**: Oregon (US West)
   - **Health Check Path**: `/healthz`
   - **Auto-Deploy**: Yes (for main branch)

5. **Click "Environment" tab**
6. **Add/Update these variables:**
   ```
   APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
   DB_PASSWORD=Supreeeth24#
   GROQ_API_KEY=your_groq_api_key_here
   ```

7. **For RAG Service** (`rag-service`):
   - **Runtime**: Docker
   - **Dockerfile Path**: `./python-rag/Dockerfile`
   - **Docker Context**: `./python-rag`
   - **Health Check Path**: `/health`
   - **Environment Variables**:
     ```
     DB_PASSWORD=Supreeeth24#
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```

### Step 3: Deploy Code

```bash
# Add all files
git add .

# Commit changes
git commit -m "feat: Add Docker deployment with Nginx, PHP-FPM, and RAG service"

# Push to main branch
git push origin main
```

### Step 4: Monitor Deployment

1. **Watch Build Logs** in Render Dashboard
2. **Expected Build Time**: 5-10 minutes
3. **Look for**:
   - ✅ Docker image built successfully
   - ✅ PHP dependencies installed
   - ✅ Node dependencies installed
   - ✅ Vite assets built
   - ✅ Container started

### Step 5: Verify Deployment

After deployment completes, test these endpoints:

```bash
# Health check (should return 200 OK)
curl https://college-placement-portals.onrender.com/healthz

# Main application (should load landing page)
curl https://college-placement-portals.onrender.com/

# RAG service health check
curl https://rag-service.onrender.com/health
```

---

## ✅ Testing & Verification

### 1. Health Check Test
```bash
curl -i https://college-placement-portals.onrender.com/healthz
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-11T02:21:37+00:00",
  "service": "college-placement-portal",
  "database": "connected",
  "app_env": "production"
}
```

### 2. Database Connection Test
```bash
curl https://college-placement-portals.onrender.com/test-db
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Connected to Supabase PostgreSQL successfully!",
  "version": "PostgreSQL 15.x..."
}
```

### 3. Frontend Assets Test
Visit: https://college-placement-portals.onrender.com

**Check for:**
- ✅ Page loads without errors
- ✅ CSS styling applied correctly
- ✅ No 404 errors in browser console
- ✅ Tailwind CSS classes working

### 4. RAG Service Test
```bash
curl https://rag-service.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "rag-service",
  "chromadb": "connected"
}
```

---

## 🔧 Troubleshooting

### Issue 1: "Class not found" Errors

**Cause**: Composer autoload not optimized

**Solution**:
```bash
# SSH into Render shell (if available) or add to start.sh:
composer dump-autoload --optimize
php artisan config:clear
php artisan cache:clear
```

### Issue 2: Vite Assets Not Loading (404 errors)

**Symptoms**: 
- CSS not applied
- Console shows: `GET /build/assets/app-xxx.js 404`

**Solution**:
1. Check if `public/build` directory exists in container
2. Verify Vite build completed in logs
3. Add to Dockerfile if missing:
   ```dockerfile
   RUN npm run build
   ```

### Issue 3: Session/CSRF Token Mismatch

**Cause**: Proxy headers not trusted

**Solution**: Already fixed in `bootstrap/app.php`:
```php
$middleware->trustProxies(at: '*');
```

**Verify in .env:**
```bash
SESSION_DRIVER=cookie
SESSION_SECURE_COOKIE=true
TRUSTED_PROXIES=*
```

### Issue 4: Database Connection Failed

**Symptoms**: 
- Health check returns `database: disconnected`
- Error: `SQLSTATE[08006]`

**Solutions**:

**A. Check Connection Pooler Port:**
```bash
DB_PORT=6543  # Use connection pooler, not direct port 5432
```

**B. Verify SSL Mode:**
```bash
DB_SSLMODE=require  # Required for Supabase
```

**C. Check Username Format:**
```bash
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl  # Include project ref
```

**D. Test Connection Manually:**
```bash
# In Render shell
php artisan tinker
>>> DB::connection()->getPdo();
```

### Issue 5: 500 Internal Server Error

**Check Logs:**
```bash
# In Render Dashboard → Logs tab
# Look for PHP errors
```

**Common Causes:**
1. Missing APP_KEY
2. Database connection failed
3. Storage permissions issue
4. Missing PHP extensions

**Quick Fix:**
```bash
# Verify APP_KEY is set
echo $APP_KEY

# Check storage permissions (should be 775)
ls -la storage/

# Verify PHP extensions
php -m | grep pdo_pgsql
```

### Issue 6: Nginx 502 Bad Gateway

**Cause**: PHP-FPM not running or crashed

**Solution**:
```bash
# Check supervisor logs
tail -f /var/log/supervisor/supervisord.log

# Restart PHP-FPM
supervisorctl restart php-fpm
```

### Issue 7: Container Keeps Restarting

**Check**:
1. Health check endpoint responding
2. Port 8000 is accessible
3. Startup script completed successfully

**Debug**:
```bash
# View startup logs
docker logs <container_id>

# Check if migrations failed
grep "migrate" /var/log/supervisor/supervisord.log
```

---

## 📝 Post-Deployment Commands

### Generate New APP_KEY
```bash
# Run in Render shell
php artisan key:generate --show
# Copy output and add to Render environment variables
```

### Run Database Migrations
```bash
php artisan migrate --force
```

### Clear All Caches
```bash
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
```

### Optimize for Production
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
composer dump-autoload --optimize
```

### Check Database Connection
```bash
php artisan db:show
```

### View Application Info
```bash
php artisan about
```

### Sync RAG Knowledge Base
```bash
# Call from Laravel
curl -X POST https://college-placement-portals.onrender.com/admin/rag/sync
```

---

## 🔗 Important URLs

- **Main Application**: https://college-placement-portals.onrender.com
- **Health Check**: https://college-placement-portals.onrender.com/healthz
- **DB Test**: https://college-placement-portals.onrender.com/test-db
- **RAG Service**: https://rag-service.onrender.com
- **RAG Health**: https://rag-service.onrender.com/health
- **Render Dashboard**: https://dashboard.render.com

---

## 📊 Performance Notes

### Free Tier Limitations:
- **Cold Start**: 30-60 seconds after inactivity
- **Memory**: 512 MB RAM
- **CPU**: Shared
- **Disk**: Ephemeral (resets on deploy)

### Optimization Tips:
1. Use OPcache (already configured)
2. Cache routes and config (done in start.sh)
3. Optimize Composer autoload (done in Dockerfile)
4. Use cookie sessions instead of database
5. Enable Gzip compression (configured in Nginx)

---

## 🆘 Support Checklist

If deployment fails, verify:

- [ ] APP_KEY is set in Render environment
- [ ] DB_PASSWORD is correct
- [ ] Database host uses connection pooler (port 6543)
- [ ] DB_USERNAME includes project reference
- [ ] DB_SSLMODE is set to `require`
- [ ] Docker runtime is selected
- [ ] Health check path is `/healthz`
- [ ] All required PHP extensions installed
- [ ] Vite build completed successfully
- [ ] Storage directories have correct permissions
- [ ] Nginx and PHP-FPM are running

---

## 🎉 Success Indicators

Your deployment is successful when:

✅ Health check returns `status: healthy`
✅ Database shows `connected`
✅ Landing page loads with styling
✅ No 404 errors for assets
✅ Login page accessible
✅ RAG service health check passes
✅ No errors in Render logs

---

**Last Updated**: 2025-10-11
**Version**: 1.0.0
