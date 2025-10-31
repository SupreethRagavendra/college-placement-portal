# 🚀 Render.com Docker Deployment - Complete Package

## 📦 What You Have

A **production-ready Docker deployment** for your College Placement Portal with:

### ✅ Laravel 11 Application
- **Nginx** web server (port 8000)
- **PHP 8.2-FPM** with OPcache
- **Supervisor** process manager
- **Vite** compiled assets (Tailwind CSS, Alpine.js)
- **Supabase PostgreSQL** database (connection pooler)
- **Cookie-based sessions** (no database dependency)
- **TrustProxies** middleware for Render
- **Health check** endpoint (`/healthz`)
- **Auto migrations** on startup

### ✅ Python FastAPI RAG Service
- **FastAPI** framework with Uvicorn
- **ChromaDB** vector database
- **OpenRouter AI** integration
- **Knowledge sync** with Laravel database
- **Health check** endpoint (`/health`)
- **CORS support** for cross-origin requests

### ✅ Complete Documentation
1. **QUICK_START_DOCKER.md** - Deploy in 5 minutes ⚡
2. **DOCKER_DEPLOYMENT_GUIDE.md** - Complete step-by-step guide
3. **DOCKER_DEPLOYMENT_SUMMARY.md** - Architecture overview
4. **RENDER_QUICK_REFERENCE.md** - Quick reference card
5. **TROUBLESHOOTING_DOCKER.md** - Common issues & solutions
6. **DEPLOYMENT_CHECKLIST.md** - Detailed checklist

---

## 🎯 Quick Start (5 Minutes)

### 1. Push Code
```bash
git push origin main
```

### 2. Set Environment Variables in Render

**Laravel Service** (`college-placement-portal`):
```bash
APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=
DB_PASSWORD=Supreeeth24#
GROQ_API_KEY=your_groq_api_key_here
```

**RAG Service** (`rag-service`):
```bash
DB_PASSWORD=Supreeeth24#
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Verify Settings
- Runtime: **Docker**
- Health Check: **/healthz** (Laravel) or **/health** (RAG)
- Region: **Oregon (US West)**

### 4. Wait & Test
```bash
# Test endpoints
curl https://college-placement-portals.onrender.com/healthz
curl https://rag-service.onrender.com/health

# Open in browser
open https://college-placement-portals.onrender.com/
```

---

## 📁 File Structure

```
college-placement-portal/
├── Dockerfile                          # Laravel container
├── .dockerignore                       # Build optimization
├── render.yaml                         # Both services config
│
├── docker/                             # Docker configs
│   ├── nginx/
│   │   ├── nginx.conf                 # Nginx main config
│   │   └── default.conf               # Site config
│   ├── php/
│   │   ├── php-fpm.conf              # FPM settings
│   │   └── php.ini                    # PHP settings
│   ├── supervisor/
│   │   └── supervisord.conf          # Process manager
│   └── start.sh                       # Startup script
│
├── python-rag/
│   └── Dockerfile                     # RAG service container
│
└── docs/                               # All documentation
    ├── QUICK_START_DOCKER.md
    ├── DOCKER_DEPLOYMENT_GUIDE.md
    ├── DOCKER_DEPLOYMENT_SUMMARY.md
    ├── RENDER_QUICK_REFERENCE.md
    ├── TROUBLESHOOTING_DOCKER.md
    └── DEPLOYMENT_CHECKLIST.md
```

---

## 🔧 Configuration Details

### Database Configuration (Supabase)
```yaml
Host: db.wkqbukidxmzbgwauncrl.supabase.co
Port: 6543                    # Connection Pooler (NOT 5432)
Database: postgres
Username: postgres.wkqbukidxmzbgwauncrl
SSL Mode: require             # REQUIRED
```

### Service URLs
- **Main App**: https://college-placement-portals.onrender.com
- **RAG Service**: https://rag-service.onrender.com
- **GitHub**: https://github.com/SupreethRagavendra/college-placement-portals

### Health Check Endpoints
- **Laravel**: `GET /healthz` (returns JSON with database status)
- **RAG**: `GET /health` (returns JSON with service status)

---

## 🎨 Architecture Diagram

```
┌──────────────────────────────────────────────┐
│           Render.com Platform                 │
├──────────────────────────────────────────────┤
│                                               │
│  ┌────────────────────────────────────────┐  │
│  │  Laravel Service (Docker)              │  │
│  │  ┌─────────┐  ┌─────────┐  ┌────────┐ │  │
│  │  │ Nginx   │→ │PHP-FPM  │→ │Laravel │ │  │
│  │  │ :8000   │  │         │  │        │ │  │
│  │  └─────────┘  └─────────┘  └────────┘ │  │
│  │         Managed by Supervisor          │  │
│  └────────────────────────────────────────┘  │
│                    ↓                          │
│  ┌────────────────────────────────────────┐  │
│  │  RAG Service (Docker)                  │  │
│  │  ┌─────────┐  ┌─────────┐  ┌────────┐ │  │
│  │  │Uvicorn  │→ │FastAPI  │→ │ChromaDB│ │  │
│  │  │ :8001   │  │         │  │        │ │  │
│  │  └─────────┘  └─────────┘  └────────┘ │  │
│  └────────────────────────────────────────┘  │
│                    ↓                          │
│  ┌────────────────────────────────────────┐  │
│  │  Supabase PostgreSQL (External)        │  │
│  │  Port 6543 (Connection Pooler)         │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## 🔐 Security Features

✅ **TrustProxies** - Handles Render's proxy infrastructure
✅ **HTTPS Enforced** - Automatic SSL certificates
✅ **Secure Sessions** - Cookie-based with secure flag
✅ **CSRF Protection** - Laravel's built-in protection
✅ **Database SSL** - Required for Supabase connection
✅ **Environment Variables** - Secrets not in code
✅ **OPcache** - No source code in responses

---

## 📊 Performance Optimizations

✅ **OPcache Enabled** - PHP bytecode caching
✅ **Gzip Compression** - Nginx compression
✅ **Static Asset Caching** - 1 year cache headers
✅ **Config Caching** - Laravel config/route/view cache
✅ **Composer Optimized** - Autoloader optimization
✅ **Connection Pooler** - Database connection pooling
✅ **FastCGI Buffering** - Optimized buffer sizes

---

## 🧪 Testing Commands

### Test Locally with Docker
```bash
# Build Laravel image
docker build -t laravel-app .

# Run Laravel container
docker run -p 8000:8000 --env-file .env laravel-app

# Build RAG image
cd python-rag
docker build -t rag-service .

# Run RAG container
docker run -p 8001:8001 --env-file .env rag-service
```

### Test Health Endpoints
```bash
# Laravel health
curl -i http://localhost:8000/healthz

# RAG health
curl -i http://localhost:8001/health
```

### Test Database Connection
```bash
# From Laravel container
docker exec -it <container_id> php artisan tinker
>>> DB::connection()->getPdo();
```

---

## 🚨 Common Issues & Quick Fixes

### Issue: 500 Internal Server Error
**Fix**: Check APP_KEY is set in Render environment variables

### Issue: Assets Not Loading (404)
**Fix**: Wait 30 seconds for cold start, check build logs for "npm run build"

### Issue: Database Connection Failed
**Fix**: Use port 6543 (not 5432), verify DB_SSLMODE=require

### Issue: CSRF Token Mismatch
**Fix**: Clear cookies, verify SESSION_DRIVER=cookie

### Issue: Container Restart Loop
**Fix**: Check health endpoint is responding, verify port 8000 is listening

**Full troubleshooting**: See `TROUBLESHOOTING_DOCKER.md`

---

## 📈 Monitoring & Maintenance

### Health Checks
- Render automatically monitors health endpoints
- Restarts container if health check fails
- View status in Render Dashboard

### Logs
- **Access Logs**: Render Dashboard → Logs tab
- **Error Logs**: Stderr output in Render logs
- **Laravel Logs**: `storage/logs/laravel.log`

### Updates
```bash
# Deploy updates
git push origin main

# Render auto-deploys on push
# Monitor in Dashboard → Events tab
```

---

## 🎓 Learning Resources

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Render
- [Render Documentation](https://render.com/docs)
- [Docker Deployment Guide](https://render.com/docs/docker)

### Laravel
- [Laravel Deployment](https://laravel.com/docs/deployment)
- [Laravel Optimization](https://laravel.com/docs/deployment#optimization)

### Nginx
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PHP-FPM Configuration](https://www.php.net/manual/en/install.fpm.configuration.php)

---

## 🎯 Next Steps

After successful deployment:

1. **Monitor Performance**
   - Set up uptime monitoring
   - Track response times
   - Monitor error rates

2. **Optimize Further**
   - Consider upgrading from free tier
   - Add Redis for caching (optional)
   - Set up CDN for assets (optional)

3. **Backup Strategy**
   - Regular database backups
   - Export environment variables
   - Document custom configurations

4. **Security Hardening**
   - Enable 2FA on all services
   - Regular dependency updates
   - Security audit logs

---

## 📞 Support

### Documentation
- Start with: `QUICK_START_DOCKER.md`
- Detailed guide: `DOCKER_DEPLOYMENT_GUIDE.md`
- Issues: `TROUBLESHOOTING_DOCKER.md`

### External Resources
- **Render Support**: support@render.com
- **Render Status**: https://status.render.com
- **GitHub Issues**: Repository issues tab

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables set in Render
- [ ] Service settings verified (Docker runtime, health checks)
- [ ] Build completed successfully
- [ ] Health checks passing
- [ ] Application loads with styling
- [ ] Database connection working
- [ ] RAG service responding

---

## 🎉 Success!

Your College Placement Portal is now deployed with:

✅ **Production-ready infrastructure**
✅ **Docker containerization**
✅ **Auto-deployment pipeline**
✅ **Health monitoring**
✅ **Performance optimization**
✅ **Comprehensive documentation**

**Main URL**: https://college-placement-portals.onrender.com
**RAG Service**: https://rag-service.onrender.com

---

**Version**: 1.0.0
**Last Updated**: 2025-10-11
**Status**: Production Ready 🚀
