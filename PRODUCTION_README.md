# College Placement Portal - Production Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [RAG Chatbot Setup](#rag-chatbot-setup)
- [Production Deployment](#production-deployment)
- [Security Configuration](#security-configuration)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### For Development
```bash
# 1. Clone and install
git clone <repository-url>
cd college-placement-portal
composer install
npm install

# 2. Configure environment
copy .env.example .env
# Edit .env with your database and email settings

# 3. Setup database
php artisan migrate --seed

# 4. Start servers
php artisan serve          # Laravel (port 8000)
npm run dev               # Vite (port 5173)

# 5. Start RAG chatbot (optional)
cd python-rag
pip install -r requirements.txt
python openrouter_rag_service.py
```

### For Production
```bash
# 1. Set production environment
APP_ENV=production
APP_DEBUG=false

# 2. Optimize
php artisan optimize
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 3. Start services
php artisan serve --host=0.0.0.0 --port=8000
```

---

## 💻 System Requirements

### Backend
- **PHP:** 8.1 or higher
- **Composer:** 2.x
- **Database:** PostgreSQL 13+ (Supabase) or MySQL 8+
- **Extensions:** PDO, pgsql, mbstring, openssl, tokenizer, xml, ctype, json

### Frontend
- **Node.js:** 18.x or higher
- **NPM:** 9.x or higher

### RAG Chatbot (Optional)
- **Python:** 3.9 or higher
- **pip:** Latest version
- **OpenRouter API Key:** Required for AI features

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd college-placement-portal
```

### 2. Install Dependencies
```bash
# PHP dependencies
composer install --no-dev --optimize-autoloader

# Node dependencies
npm install
npm run build
```

### 3. Environment Configuration
```bash
# Copy environment file
copy .env.example .env

# Generate application key
php artisan key:generate
```

### 4. Configure .env File
```env
# Application
APP_NAME="College Placement Portal"
APP_ENV=production
APP_DEBUG=false
APP_URL=http://your-domain.com

# Database (Supabase PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=your-project.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=your-password

# Email (SMTP)
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=your-email@gmail.com
MAIL_FROM_NAME="${APP_NAME}"

# Session
SESSION_DRIVER=file
SESSION_LIFETIME=120

# Cache
CACHE_DRIVER=file
QUEUE_CONNECTION=database
```

### 5. Database Setup
```bash
# Run migrations
php artisan migrate

# Seed initial data (optional)
php artisan db:seed
```

---

## 🤖 RAG Chatbot Setup

The RAG (Retrieval-Augmented Generation) chatbot provides AI-powered student assistance.

### 1. Install Python Dependencies
```bash
cd python-rag
pip install -r requirements.txt
```

### 2. Configure OpenRouter API
Add to `.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
RAG_SERVICE_URL=http://localhost:8001
```

Get your API key from: https://openrouter.ai/keys

### 3. Start RAG Service
```bash
# Windows
cd python-rag
start_openrouter_rag.bat

# Linux/Mac
cd python-rag
python openrouter_rag_service.py
```

### 4. Verify Service
```bash
# Check health endpoint
curl http://localhost:8001/health
```

### Features
- **Mode 1 (RAG Active):** Full AI-powered responses with context
- **Mode 2 (Limited Mode):** Database queries with pattern matching
- **Mode 3 (Offline):** Basic hardcoded responses

---

## 🚀 Production Deployment

### Pre-Deployment Checklist

#### 1. Environment Configuration
```env
APP_ENV=production
APP_DEBUG=false
APP_KEY=<generate-with-artisan>
```

#### 2. Security Settings
```env
SESSION_SECURE_COOKIE=true
SESSION_SAME_SITE=strict
SANCTUM_STATEFUL_DOMAINS=your-domain.com
```

#### 3. Optimize Application
```bash
# Clear all caches
php artisan optimize:clear

# Cache configuration
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Optimize autoloader
composer install --optimize-autoloader --no-dev
```

#### 4. Build Assets
```bash
npm run build
```

#### 5. Set Permissions
```bash
# Linux/Mac
chmod -R 755 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache

# Windows (run as Administrator)
icacls storage /grant Users:F /T
icacls bootstrap\cache /grant Users:F /T
```

### Deployment Steps

#### Option 1: Traditional Server
```bash
# 1. Upload files via FTP/SFTP
# 2. SSH into server
# 3. Run deployment commands
composer install --no-dev
php artisan migrate --force
php artisan optimize
```

#### Option 2: Docker
```bash
# Build image
docker build -t college-placement-portal .

# Run container
docker run -d -p 8000:8000 college-placement-portal
```

#### Option 3: Cloud Platform (Heroku, AWS, etc.)
- Follow platform-specific deployment guides
- Ensure environment variables are set
- Configure database connection
- Set up scheduled tasks for queue workers

---

## 🔒 Security Configuration

### 1. Application Security
```env
# Strong APP_KEY
php artisan key:generate

# Disable debug mode
APP_DEBUG=false

# Secure sessions
SESSION_SECURE_COOKIE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax
```

### 2. Database Security
```env
# Use strong passwords
DB_PASSWORD=<complex-password>

# Enable SSL for Supabase
DB_SSLMODE=require
```

### 3. CORS Configuration
Edit `config/cors.php`:
```php
'allowed_origins' => [env('APP_URL')],
'allowed_methods' => ['GET', 'POST', 'PUT', 'DELETE'],
'allowed_headers' => ['Content-Type', 'Authorization'],
```

### 4. Rate Limiting
Already configured in `app/Http/Kernel.php`:
- Login: 5 attempts per minute
- Registration: 3 attempts per minute
- Chatbot: 10 requests per minute

### 5. HTTPS Configuration
```bash
# Force HTTPS in production
# Add to .env
FORCE_HTTPS=true
```

### 6. Security Headers
Already implemented via middleware:
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000

---

## 🔧 Maintenance

### Clear Cache
```bash
# Clear all caches
php artisan optimize:clear

# Clear specific caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
```

### Database Maintenance
```bash
# Run migrations
php artisan migrate

# Rollback last migration
php artisan migrate:rollback

# Reset database (WARNING: Deletes all data)
php artisan migrate:fresh --seed
```

### Queue Management
```bash
# Start queue worker
php artisan queue:work

# Process failed jobs
php artisan queue:retry all

# Clear failed jobs
php artisan queue:flush
```

### Logs
```bash
# View logs
tail -f storage/logs/laravel.log

# Clear logs
> storage/logs/laravel.log
```

### Backup
```bash
# Database backup (PostgreSQL)
pg_dump -h host -U user -d database > backup.sql

# Files backup
tar -czf backup.tar.gz storage/ public/uploads/
```

### Validation Script
```bash
# Run production validation
php validate-production.php
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check database credentials in .env
# Test connection
php artisan tinker
>>> DB::connection()->getPdo();
```

#### 2. Permission Errors
```bash
# Fix storage permissions
chmod -R 775 storage bootstrap/cache
```

#### 3. 500 Internal Server Error
```bash
# Check logs
tail -f storage/logs/laravel.log

# Clear cache
php artisan optimize:clear
```

#### 4. RAG Chatbot Not Working
```bash
# Check if service is running
curl http://localhost:8001/health

# Restart service
cd python-rag
python openrouter_rag_service.py

# Check API key in .env
OPENROUTER_API_KEY=sk-or-v1-...
```

#### 5. Email Not Sending
```bash
# Test email configuration
php artisan tinker
>>> Mail::raw('Test', function($msg) { $msg->to('test@example.com'); });

# Check SMTP settings in .env
# For Gmail: Enable "Less secure app access" or use App Password
```

#### 6. Session Issues
```bash
# Clear sessions
php artisan session:clear

# Change session driver in .env
SESSION_DRIVER=file  # or database
```

### Performance Issues
```bash
# Enable OPcache (php.ini)
opcache.enable=1
opcache.memory_consumption=128
opcache.max_accelerated_files=10000

# Use Redis for cache (optional)
CACHE_DRIVER=redis
SESSION_DRIVER=redis
```

---

## 📞 Support

### Documentation
- **Main README:** README.md
- **Deployment Checklist:** DEPLOYMENT_CHECKLIST.md
- **Environment Setup:** ENVIRONMENT_SETUP.md

### Logs Location
- **Application Logs:** `storage/logs/laravel.log`
- **Web Server Logs:** Check your web server configuration
- **RAG Service Logs:** Console output when running Python service

### Health Checks
```bash
# Application health
curl http://localhost:8000

# RAG service health
curl http://localhost:8001/health

# Database connection
php artisan tinker
>>> DB::connection()->getPdo();
```

---

## 📄 License

This project is proprietary software. All rights reserved.

---

## 🎯 Quick Commands Reference

```bash
# Development
php artisan serve
npm run dev

# Production
php artisan optimize
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Maintenance
php artisan optimize:clear
php artisan migrate
php artisan queue:work

# Validation
php validate-production.php

# RAG Chatbot
cd python-rag && python openrouter_rag_service.py
```

---

**Last Updated:** 2025-01-10
**Version:** 1.0.0
