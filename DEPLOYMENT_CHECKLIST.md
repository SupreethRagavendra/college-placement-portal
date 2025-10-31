# ✅ Render Docker Deployment Checklist

Complete checklist for deploying College Placement Portal + RAG Service to Render using Docker.

## 📋 Pre-Deployment Checklist

### Repository Preparation
- [ ] All code is committed to GitHub repository
- [ ] `.env` file is not committed (check .gitignore)
- [ ] `render.yaml` file is created and committed
- [ ] `Dockerfile` is created for Laravel
- [ ] `python-rag/Dockerfile` is created for RAG service
- [ ] `.dockerignore` file is created
- [ ] All Docker config files in `docker/` directory
- [ ] `.env.example` file exists with all required variables

### Environment Variables Preparation
- [ ] Gmail app password generated (or SendGrid API key ready)
- [ ] Supabase database credentials available
- [ ] Application key ready to generate
- [ ] All required environment variables documented

## 🚀 Deployment Steps

### Step 1: Create Render Account
- [ ] Sign up at [render.com](https://render.com)
- [ ] Verify email address
- [ ] Connect GitHub account

### Step 2: Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Select repository: `college-placement-portal`
- [ ] Choose branch: `main` (or your default branch)

### Step 3: Configure Laravel Service Settings
- [ ] **Name**: `college-placement-portal`
- [ ] **Runtime**: `Docker`
- [ ] **Region**: `Oregon (US West)`
- [ ] **Plan**: `Free`
- [ ] **Health Check Path**: `/healthz`
- [ ] **Auto-Deploy**: `Yes` (main branch)
- [ ] Dockerfile will handle build automatically

### Step 4: Set Laravel Environment Variables (CRITICAL)
**Only these need to be set manually in Render:**
- [ ] `APP_KEY` = `base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4=`
- [ ] `DB_PASSWORD` = `Supreeeth24#`
- [ ] `GROQ_API_KEY` = `your_groq_api_key_here`

**Note**: All other variables are configured in `render.yaml`

### Step 5: Create RAG Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect same GitHub repository
- [ ] **Name**: `rag-service`
- [ ] **Runtime**: `Docker`
- [ ] **Dockerfile Path**: `./python-rag/Dockerfile`
- [ ] **Docker Context**: `./python-rag`
- [ ] **Region**: `Oregon (US West)`
- [ ] **Plan**: `Free`
- [ ] **Health Check Path**: `/health`
- [ ] **Auto-Deploy**: `Yes` (main branch)

### Step 6: Set RAG Service Environment Variables (CRITICAL)
**Only these need to be set manually:**
- [ ] `DB_PASSWORD` = `Supreeeth24#`
- [ ] `OPENROUTER_API_KEY` = `your_openrouter_api_key_here`

**Note**: All other variables are configured in `render.yaml`

### Step 7: Deploy Both Services
- [ ] Push code to GitHub: `git push origin main`
- [ ] Both services will auto-deploy
- [ ] Wait for builds to complete (10-15 minutes total)
- [ ] Check build logs for any errors
- [ ] Note both deployment URLs

### Step 8: Verify Deployment
**Test Laravel Service:**
- [ ] Health check: `https://college-placement-portals.onrender.com/healthz`
- [ ] Database test: `https://college-placement-portals.onrender.com/test-db`
- [ ] Main site: `https://college-placement-portals.onrender.com/`

**Test RAG Service:**
- [ ] Health check: `https://rag-service.onrender.com/health`

### Step 9: Database Migrations (Auto-runs in start.sh)
**Migrations run automatically on startup, but verify:**
- [ ] Check logs for "Running database migrations"
- [ ] Check logs for "✅ Laravel application ready!"
- [ ] If needed, run manually in Shell: `php artisan migrate --force`

### Step 10: Test Full Application
- [ ] Landing page loads with styling
- [ ] Registration form works
- [ ] Login works
- [ ] Admin dashboard accessible
- [ ] Student dashboard accessible
- [ ] RAG chatbot responds (if configured)

## 🧪 Post-Deployment Testing

### Functional Testing
- [ ] Home page loads
- [ ] Registration form works
- [ ] Email verification works
- [ ] Login works for both admin and student
- [ ] Dashboard loads for both roles
- [ ] All navigation links work
- [ ] Forms submit correctly
- [ ] Error handling works

### Performance Testing
- [ ] Page load times are acceptable
- [ ] No JavaScript errors in console
- [ ] CSS loads correctly
- [ ] Images load properly
- [ ] Mobile responsiveness works

### Security Testing
- [ ] HTTPS is enabled
- [ ] Sensitive data is not exposed
- [ ] CSRF protection works
- [ ] Authentication is required for protected routes
- [ ] Role-based access control works

## 🔧 Troubleshooting Common Issues

### Build Failures
- [ ] Check PHP version compatibility
- [ ] Verify all dependencies in composer.json
- [ ] Check build logs for specific errors
- [ ] Ensure all required files are committed

### Database Connection Issues
- [ ] Verify Supabase credentials
- [ ] Check SSL mode settings
- [ ] Ensure database is accessible
- [ ] Test connection in Shell

### Email Issues
- [ ] Verify SMTP credentials
- [ ] Check email service limits
- [ ] Test with different email providers
- [ ] Check email logs

### Asset Loading Issues
- [ ] Ensure npm run build completes
- [ ] Check file permissions
- [ ] Verify asset paths
- [ ] Clear browser cache

## 📊 Performance Optimization

### After Successful Deployment
- [ ] Enable caching: `php artisan config:cache`
- [ ] Optimize routes: `php artisan route:cache`
- [ ] Cache views: `php artisan view:cache`
- [ ] Optimize autoloader: `composer install --optimize-autoloader`

### Monitoring Setup
- [ ] Set up uptime monitoring
- [ ] Monitor response times
- [ ] Track error rates
- [ ] Set up log monitoring

## 🔒 Security Checklist

- [ ] Environment variables are secure
- [ ] No sensitive data in logs
- [ ] HTTPS is enforced
- [ ] Strong passwords used
- [ ] 2FA enabled on all services
- [ ] Regular security updates planned

## 📈 Scaling Considerations

### Free Tier Limitations
- [ ] 750 hours/month limit
- [ ] Sleeps after 15 minutes of inactivity
- [ ] 512MB RAM limit
- [ ] No custom domains on free tier

### Upgrade Options
- [ ] Starter plan: $7/month (always on)
- [ ] Standard plan: $25/month (better performance)
- [ ] Pro plan: $85/month (production ready)

## 🎯 Success Criteria

Your deployment is successful when:
- [ ] Application loads without errors
- [ ] All authentication features work
- [ ] Email verification functions properly
- [ ] Database operations work correctly
- [ ] Performance is acceptable
- [ ] Security measures are in place

## 📞 Support Resources

- [Render Documentation](https://render.com/docs)
- [Laravel Deployment Guide](https://laravel.com/docs/deployment)
- [Supabase Documentation](https://supabase.com/docs)
- [Gmail SMTP Setup](https://support.google.com/mail/answer/185833)

---

**Deployment URL**: `https://your-app-name.onrender.com`

**Admin Login**:
- Email: `admin@portal.com`
- Password: `Admin@123`

**Next Steps**: After successful deployment, consider setting up monitoring, backups, and regular maintenance procedures.
