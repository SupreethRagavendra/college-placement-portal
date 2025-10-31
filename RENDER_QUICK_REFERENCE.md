# 🚀 Render Deployment - Quick Reference Card

## 📦 Pre-Deployment Checklist

```bash
# 1. Generate APP_KEY (if needed)
php artisan key:generate --show

# 2. Test locally with Docker
docker build -t laravel-app .
docker run -p 8000:8000 laravel-app

# 3. Commit and push
git add .
git commit -m "feat: Docker deployment ready"
git push origin main
```

---

## 🔐 Required Environment Variables

### Laravel Service
```bash
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD=Supreeeth24#
GROQ_API_KEY=your_groq_api_key_here
```

### RAG Service
```bash
DB_PASSWORD=Supreeeth24#
OPENROUTER_API_KEY=your_key_here
```

---

## ⚙️ Render Dashboard Settings

### Laravel Service (`college-placement-portal`)
- **Runtime**: Docker
- **Region**: Oregon (US West)
- **Health Check Path**: `/healthz`
- **Auto-Deploy**: Yes (main branch)

### RAG Service (`rag-service`)
- **Runtime**: Docker
- **Dockerfile Path**: `./python-rag/Dockerfile`
- **Docker Context**: `./python-rag`
- **Health Check Path**: `/health`
- **Auto-Deploy**: Yes (main branch)

---

## 🧪 Testing Endpoints

```bash
# Health check
curl https://college-placement-portals.onrender.com/healthz

# Database test
curl https://college-placement-portals.onrender.com/test-db

# Main site
curl https://college-placement-portals.onrender.com/

# RAG service
curl https://rag-service.onrender.com/health
```

---

## 🔧 Common Issues & Quick Fixes

### 500 Error
```bash
# Check APP_KEY is set
# Check database credentials
# View logs in Render Dashboard
```

### Assets Not Loading
```bash
# Verify npm run build completed
# Check public/build exists
# Clear browser cache
```

### Database Connection Failed
```bash
# Use port 6543 (connection pooler)
# DB_SSLMODE=require
# DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
```

### CSRF Token Mismatch
```bash
# SESSION_DRIVER=cookie
# TRUSTED_PROXIES=*
# Clear cookies and retry
```

---

## 📝 Post-Deployment Commands

```bash
# Clear caches
php artisan config:clear && php artisan cache:clear

# Run migrations
php artisan migrate --force

# Optimize
php artisan config:cache && php artisan route:cache
```

---

## 🔗 Important Links

- **Dashboard**: https://dashboard.render.com
- **Main App**: https://college-placement-portals.onrender.com
- **RAG Service**: https://rag-service.onrender.com
- **GitHub**: https://github.com/SupreethRagavendra/college-placement-portals

---

## 📊 File Structure Reference

```
├── Dockerfile                    # Laravel container
├── render.yaml                   # Both services config
├── docker/
│   ├── nginx/
│   │   ├── nginx.conf           # Main Nginx config
│   │   └── default.conf         # Site config
│   ├── php/
│   │   ├── php-fpm.conf        # FPM pool
│   │   └── php.ini             # PHP settings
│   ├── supervisor/
│   │   └── supervisord.conf    # Process manager
│   └── start.sh                # Startup script
└── python-rag/
    └── Dockerfile              # RAG service container
```

---

## ✅ Success Indicators

- ✅ Health check returns `status: healthy`
- ✅ Landing page loads with CSS
- ✅ No 404 errors for assets
- ✅ Database connection successful
- ✅ RAG service responding

---

## 🆘 Emergency Recovery

```bash
# 1. Check Render logs
# 2. Verify environment variables
# 3. Test health endpoint
# 4. Rollback if needed (Render Dashboard → Rollback)
# 5. Check GitHub Actions (if configured)
```

---

**Quick Access**: Keep this file open during deployment!
