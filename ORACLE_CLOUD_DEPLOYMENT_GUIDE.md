# 🚀 Oracle Cloud Free Tier Deployment Guide
## College Placement Portal - Complete Setup

---

## 📋 What You'll Get (100% FREE Forever)

✅ **Ubuntu 22.04 VM** with 1GB RAM (expandable to 4GB with 2 VMs)
✅ **50GB Boot Volume** + up to 200GB total storage
✅ **10TB monthly data transfer**
✅ **Public IP address**
✅ **Full root access**
✅ **24/7 uptime**
✅ **No credit card required** (optional later)

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────┐
│     Oracle Cloud Free Tier VM          │
│  (Ubuntu 22.04 - 1GB RAM - 50GB)       │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────┐  ┌───────────────┐ │
│  │    Nginx       │→ │  PHP-FPM 8.2  │ │
│  │   Port 80/443  │  │  Laravel 12   │ │
│  └────────────────┘  └───────────────┘ │
│                                         │
│  ┌────────────────┐  ┌───────────────┐ │
│  │  Supervisor    │→ │   Python RAG  │ │
│  │  (Process Mgr) │  │  FastAPI:8001 │ │
│  └────────────────┘  └───────────────┘ │
│                                         │
└─────────────────────────────────────────┘
              ↓
    ┌──────────────────┐
    │ Supabase         │
    │ PostgreSQL       │
    │ (Free Tier)      │
    └──────────────────┘
```

---

## 📝 Part 1: Oracle Cloud Account Setup (10 min)

### Step 1: Create Oracle Cloud Account

1. **Go to**: https://www.oracle.com/cloud/free/
2. **Click**: "Start for free"
3. **Fill in**:
   - Email address
   - Country (India or your location)
   - Account name (unique identifier)
4. **Verify email**
5. **Complete account setup**:
   - Personal information
   - Phone verification (OTP)
   - Optional: Add payment method (not charged)

⚠️ **Important**: Choose your home region carefully (can't be changed later)
- **Recommended for India**: Mumbai (ap-mumbai-1)
- **For global access**: Singapore (ap-singapore-1)

### Step 2: Create Compute Instance

1. **Login** to Oracle Cloud Console: https://cloud.oracle.com
2. **Navigate**: Menu → Compute → Instances
3. **Click**: "Create Instance"

**Instance Configuration:**
```yaml
Name: college-placement-portal
Image: Ubuntu 22.04
Shape: VM.Standard.E2.1.Micro (Always Free)
  - 1 OCPU (1 core)
  - 1GB RAM
  - Ampere ARM processor

Boot Volume: 50GB (increase if needed, up to 200GB free)

Virtual Cloud Network: Create new or use default
Public IP: Assign a public IPv4 address
```

4. **SSH Keys**: 
   - Download private key (.pem file) 
   - Save as `oracle-cloud-key.pem`
   - Keep it safe!

5. **Click**: "Create"

⏱️ Wait 2-3 minutes for provisioning...

### Step 3: Configure Firewall Rules

**Open Required Ports:**

1. **Navigate**: Instance Details → Virtual Cloud Network → Security Lists
2. **Click**: Default Security List
3. **Add Ingress Rules**:

```yaml
# HTTP
Stateless: No
Source: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 80

# HTTPS
Stateless: No
Source: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 443

# Python RAG Service (optional, for external access)
Stateless: No
Source: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 8001
```

4. **Save changes**

---

## 💻 Part 2: Server Setup (20 min)

### Step 1: Connect to Your Instance

**On Windows (PowerShell):**
```powershell
# Set key permissions (if not already done)
icacls "D:\path\to\oracle-cloud-key.pem" /inheritance:r /grant:r "%USERNAME%:R"

# Connect
ssh -i "D:\path\to\oracle-cloud-key.pem" ubuntu@<YOUR_PUBLIC_IP>
```

**On Linux/Mac:**
```bash
chmod 400 oracle-cloud-key.pem
ssh -i oracle-cloud-key.pem ubuntu@<YOUR_PUBLIC_IP>
```

Replace `<YOUR_PUBLIC_IP>` with your instance's public IP from Oracle Console.

### Step 2: Update System & Configure Firewall

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Configure Ubuntu firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8001 -j ACCEPT
sudo netfilter-persistent save

# Install iptables-persistent if not installed
sudo apt install -y iptables-persistent
```

### Step 3: Install Required Software

```bash
# Install PHP 8.2 and extensions
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update
sudo apt install -y php8.2 php8.2-fpm php8.2-cli php8.2-pgsql php8.2-mbstring \
    php8.2-xml php8.2-curl php8.2-zip php8.2-gd php8.2-bcmath php8.2-opcache

# Install Nginx
sudo apt install -y nginx

# Install Node.js & NPM (Latest LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Composer
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
sudo chmod +x /usr/local/bin/composer

# Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# Install Git
sudo apt install -y git

# Install Supervisor (process manager)
sudo apt install -y supervisor

# Install PostgreSQL client (for database connections)
sudo apt install -y postgresql-client
```

### Step 4: Verify Installations

```bash
php -v          # Should show PHP 8.2.x
composer -V     # Should show Composer version
node -v         # Should show v20.x
npm -v          # Should show npm version
python3 --version  # Should show Python 3.10+
nginx -v        # Should show nginx version
```

---

## 🚀 Part 3: Deploy Laravel Application (15 min)

### Step 1: Clone Your Repository

```bash
# Create directory for applications
sudo mkdir -p /var/www
cd /var/www

# Clone your repository
sudo git clone https://github.com/YOUR_USERNAME/college-placement-portal.git
cd college-placement-portal

# Set ownership
sudo chown -R ubuntu:ubuntu /var/www/college-placement-portal
```

### Step 2: Install Dependencies

```bash
# Install PHP dependencies
composer install --no-dev --optimize-autoloader

# Install Node dependencies
npm install

# Build frontend assets
npm run build
```

⏱️ This may take 5-10 minutes on the free tier VM.

### Step 3: Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit environment file
nano .env
```

**Update these values in `.env`:**

```env
APP_NAME="College Placement Portal"
APP_ENV=production
APP_KEY=
APP_DEBUG=false
APP_URL=http://YOUR_PUBLIC_IP

# Database (Supabase)
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=6543
DB_DATABASE=postgres
DB_USERNAME=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=Supreeeth24#
DB_SSLMODE=require

# Session
SESSION_DRIVER=file
SESSION_LIFETIME=120

# Cache
CACHE_DRIVER=file
QUEUE_CONNECTION=sync

# Mail (configure if needed)
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@yourdomain.com
MAIL_FROM_NAME="${APP_NAME}"

# RAG Service
RAG_SERVICE_URL=http://localhost:8001
```

**Save** and exit (Ctrl+X, Y, Enter)

### Step 4: Generate App Key & Setup Laravel

```bash
# Generate application key
php artisan key:generate

# Create necessary directories
mkdir -p storage/framework/cache/data
mkdir -p storage/framework/sessions
mkdir -p storage/framework/views
mkdir -p storage/logs
mkdir -p bootstrap/cache

# Set permissions
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache

# Run migrations
php artisan migrate --force

# Seed admin user
php artisan db:seed --class=AdminSeeder --force

# Cache configuration for production
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

## 🌐 Part 4: Configure Nginx (10 min)

### Step 1: Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/college-placement-portal
```

**Paste this configuration:**

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name YOUR_PUBLIC_IP;  # Replace with your IP or domain
    
    root /var/www/college-placement-portal/public;
    index index.php index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/college-portal-access.log;
    error_log /var/log/nginx/college-portal-error.log;

    # Main location
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP-FPM
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        
        # Increase timeout for slow connections
        fastcgi_read_timeout 300;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
    }

    # Static assets caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Deny access to sensitive files
    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

**Save** and exit.

### Step 2: Enable Site & Test Configuration

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/college-placement-portal /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# If test passes, restart Nginx
sudo systemctl restart nginx
sudo systemctl restart php8.2-fpm

# Enable services to start on boot
sudo systemctl enable nginx
sudo systemctl enable php8.2-fpm
```

### Step 3: Verify Laravel is Working

```bash
# Check if services are running
sudo systemctl status nginx
sudo systemctl status php8.2-fpm

# Test from browser
# Open: http://YOUR_PUBLIC_IP
```

You should see your Laravel application! 🎉

---

## 🤖 Part 5: Deploy Python RAG Service (15 min)

### Step 1: Create Python Virtual Environment

```bash
cd /var/www/college-placement-portal/python-rag

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install fastapi uvicorn chromadb openai httpx sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings
```

### Step 2: Configure RAG Service Environment

```bash
# Create .env file for RAG service
nano .env
```

**Add:**

```env
# Database
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.wkqbukidxmzbgwauncrl
DB_PASSWORD=Supreeeth24#

# OpenRouter API (or your AI provider)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Service settings
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=production
```

**Save** and exit.

### Step 3: Test RAG Service Manually

```bash
# Make sure you're in the venv
source venv/bin/activate

# Test run
uvicorn app:app --host 0.0.0.0 --port 8001

# In another terminal, test:
curl http://localhost:8001/health
```

Press Ctrl+C to stop the test.

### Step 4: Create Supervisor Configuration

```bash
sudo nano /etc/supervisor/conf.d/rag-service.conf
```

**Paste:**

```ini
[program:rag-service]
process_name=%(program_name)s
command=/var/www/college-placement-portal/python-rag/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8001
directory=/var/www/college-placement-portal/python-rag
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/rag-service.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
environment=PATH="/var/www/college-placement-portal/python-rag/venv/bin"
```

**Save** and exit.

### Step 5: Start RAG Service

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Start the service
sudo supervisorctl start rag-service

# Check status
sudo supervisorctl status rag-service

# View logs
sudo tail -f /var/log/supervisor/rag-service.log
```

### Step 6: Add RAG Service to Nginx (Optional - for external access)

```bash
sudo nano /etc/nginx/sites-available/college-placement-portal
```

**Add this location block inside the server block:**

```nginx
    # RAG Service Proxy
    location /api/rag/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

**Restart Nginx:**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Part 6: Setup SSL with Let's Encrypt (Optional - 10 min)

### Prerequisites: Domain Name Required
⚠️ **You need a domain name** (free from: Freenom, No-IP, DuckDNS)

### Step 1: Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Step 2: Obtain SSL Certificate

```bash
# Replace yourdomain.com with your actual domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts:
1. Enter email
2. Agree to terms
3. Choose whether to redirect HTTP to HTTPS (recommended: Yes)

### Step 3: Test Auto-renewal

```bash
sudo certbot renew --dry-run
```

Certificates auto-renew every 90 days! ✅

---

## 📊 Part 7: Monitoring & Maintenance

### Check Service Status

```bash
# Nginx
sudo systemctl status nginx

# PHP-FPM
sudo systemctl status php8.2-fpm

# RAG Service
sudo supervisorctl status rag-service

# View logs
sudo tail -f /var/log/nginx/college-portal-error.log
sudo tail -f /var/log/supervisor/rag-service.log
sudo tail -f /var/www/college-placement-portal/storage/logs/laravel.log
```

### Restart Services

```bash
# Restart Nginx
sudo systemctl restart nginx

# Restart PHP-FPM
sudo systemctl restart php8.2-fpm

# Restart RAG service
sudo supervisorctl restart rag-service

# Restart all
sudo systemctl restart nginx php8.2-fpm
sudo supervisorctl restart rag-service
```

### Check Disk Space

```bash
df -h
du -sh /var/www/college-placement-portal
```

### Check Memory Usage

```bash
free -h
htop  # Install with: sudo apt install htop
```

---

## 🔄 Part 8: Deploy Updates

### When You Update Code on GitHub

```bash
# SSH into your server
cd /var/www/college-placement-portal

# Pull latest changes
git pull origin main

# Update PHP dependencies (if composer.json changed)
composer install --no-dev --optimize-autoloader

# Update Node dependencies (if package.json changed)
npm install
npm run build

# Run migrations (if new migrations)
php artisan migrate --force

# Clear and rebuild cache
php artisan config:clear
php artisan cache:clear
php artisan view:clear
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Restart services
sudo systemctl restart php8.2-fpm
sudo supervisorctl restart rag-service
```

### Create Deployment Script

```bash
nano /var/www/college-placement-portal/deploy.sh
```

**Paste:**

```bash
#!/bin/bash
echo "🚀 Deploying updates..."

cd /var/www/college-placement-portal

# Pull changes
git pull origin main

# Update dependencies
composer install --no-dev --optimize-autoloader
npm install
npm run build

# Run migrations
php artisan migrate --force

# Clear cache
php artisan config:clear
php artisan cache:clear
php artisan view:clear

# Rebuild cache
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Set permissions
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache

# Restart services
sudo systemctl restart php8.2-fpm
sudo supervisorctl restart rag-service

echo "✅ Deployment complete!"
```

**Make executable:**
```bash
chmod +x /var/www/college-placement-portal/deploy.sh
```

**To deploy updates:**
```bash
./deploy.sh
```

---

## 🔐 Security Best Practices

### 1. Setup UFW Firewall

```bash
# Enable UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8001/tcp
sudo ufw enable
sudo ufw status
```

### 2. Disable Root SSH Login

```bash
sudo nano /etc/ssh/sshd_config
```

Find and change:
```
PermitRootLogin no
PasswordAuthentication no
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

### 3. Setup Automatic Security Updates

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 4. Setup Fail2Ban (Prevent Brute Force)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway
```bash
# Check PHP-FPM
sudo systemctl status php8.2-fpm
sudo systemctl restart php8.2-fpm

# Check logs
sudo tail -f /var/log/nginx/college-portal-error.log
```

### Issue: Permission Denied
```bash
# Fix storage permissions
cd /var/www/college-placement-portal
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

### Issue: Database Connection Failed
```bash
# Test connection
php artisan tinker
>>> DB::connection()->getPdo();

# Check .env settings
cat .env | grep DB_
```

### Issue: RAG Service Not Starting
```bash
# Check logs
sudo tail -f /var/log/supervisor/rag-service.log

# Manually test
cd /var/www/college-placement-portal/python-rag
source venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8001
```

### Issue: Out of Memory
```bash
# Check memory
free -h

# Add swap space (if needed)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Issue: Slow Performance
```bash
# Enable PHP OPcache
sudo nano /etc/php/8.2/fpm/php.ini
```

Add/uncomment:
```ini
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=10000
opcache.revalidate_freq=2
```

Restart:
```bash
sudo systemctl restart php8.2-fpm
```

---

## 🎯 Performance Optimization

### 1. Enable Gzip Compression

```bash
sudo nano /etc/nginx/nginx.conf
```

Add in `http` block:
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;
```

### 2. Enable Browser Caching

Already configured in Nginx config above! ✅

### 3. Use Redis for Caching (Optional)

```bash
# Install Redis
sudo apt install -y redis-server php8.2-redis

# Enable Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Update .env
CACHE_DRIVER=redis
SESSION_DRIVER=redis
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
```

---

## 📈 Monitoring & Uptime

### Setup Simple Uptime Monitoring

**External Services (Free):**
- ✅ **UptimeRobot** (https://uptimerobot.com) - 50 monitors free
- ✅ **Freshping** (https://freshping.io) - 50 checks free
- ✅ **StatusCake** (https://statuscake.com) - Basic monitoring free

**Setup:**
1. Sign up for free account
2. Add monitor for: `http://YOUR_IP/healthz`
3. Set check interval: 5 minutes
4. Add alert email

### Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/laravel
```

Add:
```
/var/www/college-placement-portal/storage/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 664 www-data www-data
}
```

---

## ✅ Final Checklist

- [ ] Oracle Cloud instance created and running
- [ ] Firewall ports opened (80, 443, 8001)
- [ ] Server software installed (PHP, Nginx, Node, Python)
- [ ] Laravel application deployed
- [ ] Database connection working
- [ ] Frontend assets built and loading
- [ ] Python RAG service running via Supervisor
- [ ] Nginx configured and serving application
- [ ] SSL certificate installed (if using domain)
- [ ] Deployment script created
- [ ] Security measures implemented
- [ ] Monitoring setup
- [ ] Can access application at http://YOUR_IP

---

## 🎉 Success!

Your College Placement Portal is now live on Oracle Cloud Free Tier!

### Access URLs:
- **Main Application**: `http://YOUR_PUBLIC_IP`
- **Admin Login**: `http://YOUR_PUBLIC_IP/login` (admin@portal.com / Admin@123)
- **RAG Service**: `http://YOUR_PUBLIC_IP:8001/health`

### Costs:
- **Monthly**: $0 💰
- **Forever**: $0 💰

---

## 📞 Support & Resources

### Documentation
- [Oracle Cloud Docs](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Laravel Deployment](https://laravel.com/docs/deployment)
- [Nginx Docs](https://nginx.org/en/docs/)

### Common Commands Cheat Sheet

```bash
# Check all services
sudo systemctl status nginx php8.2-fpm
sudo supervisorctl status rag-service

# View logs
sudo tail -f /var/log/nginx/college-portal-error.log
sudo tail -f /var/www/college-placement-portal/storage/logs/laravel.log
sudo tail -f /var/log/supervisor/rag-service.log

# Restart services
sudo systemctl restart nginx php8.2-fpm
sudo supervisorctl restart rag-service

# Deploy updates
cd /var/www/college-placement-portal && ./deploy.sh

# Check disk space
df -h

# Check memory
free -h

# Monitor real-time
htop
```

---

## 🎓 Next Steps

1. **Domain Name** - Get a free domain and setup DNS
2. **SSL Certificate** - Enable HTTPS with Let's Encrypt
3. **Backup Strategy** - Setup automated backups
4. **Monitoring** - Configure uptime monitoring
5. **Email Service** - Setup SMTP for email notifications
6. **CDN** - Consider CloudFlare for better performance

---

**Version**: 1.0.0
**Last Updated**: October 31, 2025
**Status**: Production Ready 🚀

**Total Setup Time**: ~60-90 minutes
**Monthly Cost**: $0 (FREE FOREVER!)

