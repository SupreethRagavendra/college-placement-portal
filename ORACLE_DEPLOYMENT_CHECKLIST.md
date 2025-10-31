# ✅ Oracle Cloud Deployment Checklist

## Pre-Deployment Preparation

### Before You Start:
- [ ] Have email address ready for Oracle account
- [ ] Have phone number for SMS verification
- [ ] Have GitHub repository URL ready
- [ ] Have Supabase database credentials ready
- [ ] Set aside 60-90 minutes uninterrupted time
- [ ] Have terminal/SSH client ready (PowerShell/Terminal)

---

## Phase 1: Oracle Cloud Account (10 minutes)

### Account Creation:
- [ ] Go to https://www.oracle.com/cloud/free/
- [ ] Click "Start for free"
- [ ] Fill in personal details
- [ ] Verify email (check inbox)
- [ ] Complete phone verification (SMS OTP)
- [ ] Choose home region (Mumbai/Singapore for Asia)
- [ ] Skip credit card (optional)
- [ ] Complete account setup
- [ ] Login to Oracle Cloud Console

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 2: Create VM Instance (5 minutes)

### Instance Configuration:
- [ ] Navigate to: Menu → Compute → Instances
- [ ] Click "Create Instance"
- [ ] Name: `college-placement-portal`
- [ ] Image: Select "Ubuntu 22.04"
- [ ] Shape: "VM.Standard.E2.1.Micro" (Always Free eligible)
- [ ] Verify: 1 OCPU, 1GB RAM shown
- [ ] Boot Volume: 50GB (or more if needed)
- [ ] Download SSH private key (.pem file)
- [ ] Save key as: `oracle-cloud-key.pem`
- [ ] Note down Public IP address: `___________________`
- [ ] Click "Create"
- [ ] Wait for "Running" status (2-3 minutes)

**Public IP Address:** `___________________`

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 3: Configure Firewall (5 minutes)

### Security List Configuration:
- [ ] Go to Instance Details page
- [ ] Click on VCN (Virtual Cloud Network) name
- [ ] Click "Security Lists"
- [ ] Click "Default Security List"
- [ ] Click "Add Ingress Rules"

### Add These Rules:

**Rule 1 - HTTP:**
- [ ] Source: `0.0.0.0/0`
- [ ] IP Protocol: TCP
- [ ] Destination Port: `80`
- [ ] Click "Add Ingress Rules"

**Rule 2 - HTTPS:**
- [ ] Source: `0.0.0.0/0`
- [ ] IP Protocol: TCP
- [ ] Destination Port: `443`
- [ ] Click "Add Ingress Rules"

**Rule 3 - RAG Service:**
- [ ] Source: `0.0.0.0/0`
- [ ] IP Protocol: TCP
- [ ] Destination Port: `8001`
- [ ] Click "Add Ingress Rules"

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 4: Connect to Server (5 minutes)

### Windows (PowerShell):
- [ ] Open PowerShell
- [ ] Navigate to folder with `oracle-cloud-key.pem`
- [ ] Set permissions (if needed): `icacls oracle-cloud-key.pem /inheritance:r /grant:r "%USERNAME%:R"`
- [ ] Connect: `ssh -i oracle-cloud-key.pem ubuntu@YOUR_PUBLIC_IP`
- [ ] Type "yes" when prompted about authenticity
- [ ] Verify you see Ubuntu welcome message

### Linux/Mac:
- [ ] Open Terminal
- [ ] Set permissions: `chmod 400 oracle-cloud-key.pem`
- [ ] Connect: `ssh -i oracle-cloud-key.pem ubuntu@YOUR_PUBLIC_IP`
- [ ] Type "yes" when prompted
- [ ] Verify connection successful

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 5: Automated Setup (40 minutes)

### Option A: Use Our Automated Script (Recommended)

**Download and run:**
```bash
curl -o setup.sh https://raw.githubusercontent.com/YOUR_USERNAME/college-placement-portal/main/oracle-setup.sh
chmod +x setup.sh
./setup.sh
```

- [ ] Script downloaded successfully
- [ ] Script running
- [ ] Provide GitHub repository URL when prompted
- [ ] Provide database credentials when prompted
- [ ] Wait for completion (30-40 minutes)
- [ ] Verify "Setup Complete!" message

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### Option B: Manual Setup (If script fails)

#### Step 1: System Update
- [ ] `sudo apt update && sudo apt upgrade -y` (5 min)
- [ ] Configure firewall rules (run commands from guide)
- [ ] Install iptables-persistent

#### Step 2: Install Software
- [ ] Add PHP repository
- [ ] Install PHP 8.2 and extensions
- [ ] Install Nginx
- [ ] Install Node.js 20.x
- [ ] Install Composer
- [ ] Install Python 3 and pip
- [ ] Install Git and Supervisor
- [ ] Install PostgreSQL client
- [ ] Verify all installations: `php -v`, `node -v`, `composer -V`

#### Step 3: Clone Repository
- [ ] `sudo mkdir -p /var/www`
- [ ] `cd /var/www`
- [ ] Clone your repository
- [ ] Set ownership: `sudo chown -R ubuntu:ubuntu /var/www/college-placement-portal`
- [ ] `cd college-placement-portal`

#### Step 4: Install Dependencies
- [ ] `composer install --no-dev --optimize-autoloader` (5-10 min)
- [ ] `npm install` (5-10 min)
- [ ] `npm run build` (2-3 min)
- [ ] Verify public/build/ directory exists

#### Step 5: Configure Environment
- [ ] `cp .env.example .env`
- [ ] `nano .env` (edit configuration)
- [ ] Update APP_URL with public IP
- [ ] Set APP_ENV=production
- [ ] Set APP_DEBUG=false
- [ ] Configure database settings
- [ ] Save and exit (Ctrl+X, Y, Enter)
- [ ] `php artisan key:generate`
- [ ] Create storage directories
- [ ] Set permissions on storage and bootstrap/cache
- [ ] `php artisan migrate --force`
- [ ] `php artisan db:seed --class=AdminSeeder --force`
- [ ] Cache configuration

#### Step 6: Configure Nginx
- [ ] Create Nginx config file
- [ ] Copy configuration from guide
- [ ] Enable site
- [ ] Remove default site
- [ ] Test: `sudo nginx -t`
- [ ] Restart: `sudo systemctl restart nginx`
- [ ] Enable: `sudo systemctl enable nginx`

#### Step 7: Configure PHP-FPM
- [ ] Restart: `sudo systemctl restart php8.2-fpm`
- [ ] Enable: `sudo systemctl enable php8.2-fpm`
- [ ] Check status: `sudo systemctl status php8.2-fpm`

#### Step 8: Setup Python RAG
- [ ] `cd /var/www/college-placement-portal/python-rag`
- [ ] Create venv: `python3 -m venv venv`
- [ ] Activate: `source venv/bin/activate`
- [ ] Install dependencies
- [ ] Create .env file
- [ ] Configure database connection
- [ ] Test manually
- [ ] Create Supervisor config
- [ ] Start service
- [ ] Verify running

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 6: Verification (5 minutes)

### Check Services:
- [ ] **Nginx:** `sudo systemctl status nginx` → Shows "active (running)"
- [ ] **PHP-FPM:** `sudo systemctl status php8.2-fpm` → Shows "active (running)"
- [ ] **RAG Service:** `sudo supervisorctl status rag-service` → Shows "RUNNING"

### Test in Browser:
- [ ] Open: `http://YOUR_PUBLIC_IP`
- [ ] Homepage loads successfully
- [ ] CSS and styling appear correctly
- [ ] Images load properly
- [ ] Click "Login" → Login page loads
- [ ] Test admin login:
  - Email: `admin@portal.com`
  - Password: `Admin@123`
- [ ] Successfully login to admin dashboard
- [ ] Check dashboard loads with data

### Test RAG Service:
- [ ] Open: `http://YOUR_PUBLIC_IP:8001/health`
- [ ] Should see JSON response with status
- [ ] Or: `curl http://YOUR_PUBLIC_IP:8001/health`

### Check Logs (if issues):
- [ ] Nginx errors: `sudo tail -f /var/log/nginx/college-portal-error.log`
- [ ] Laravel logs: `sudo tail -f /var/www/college-placement-portal/storage/logs/laravel.log`
- [ ] RAG logs: `sudo tail -f /var/log/supervisor/rag-service.log`

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 7: Security & Optimization (10 minutes)

### Security:
- [ ] Setup UFW firewall
- [ ] Disable root SSH login
- [ ] Setup automatic updates
- [ ] Install Fail2Ban
- [ ] Review security checklist in guide

### Optimization:
- [ ] Enable PHP OPcache (should be done by script)
- [ ] Enable Gzip in Nginx
- [ ] Verify browser caching configured
- [ ] Test page load speed

### Optional - SSL Setup:
- [ ] Have domain name ready
- [ ] Point domain to public IP
- [ ] Install Certbot
- [ ] Obtain SSL certificate
- [ ] Test HTTPS access

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 8: Documentation (5 minutes)

### Save Important Information:

**Server Details:**
```
Public IP: ___________________________
SSH Key Location: _____________________
Oracle Region: ________________________
```

**Database Details:**
```
Host: _________________________________
Port: _________________________________
Database: _____________________________
Username: _____________________________
```

**Application Details:**
```
App URL: http://_______________________
Admin Email: admin@portal.com
Admin Password: Admin@123
RAG Service: http://___________________:8001
```

**Important Files:**
```
Nginx Config: /etc/nginx/sites-available/college-placement-portal
PHP Config: /etc/php/8.2/fpm/php.ini
App Directory: /var/www/college-placement-portal
Logs: /var/log/nginx/college-portal-error.log
```

**Useful Commands:**
```
Check services: ./check-services.sh
Deploy updates: ./deploy.sh
View logs: sudo tail -f /var/log/nginx/college-portal-error.log
Restart all: sudo systemctl restart nginx php8.2-fpm && sudo supervisorctl restart rag-service
```

- [ ] Information saved in safe location
- [ ] SSH key backed up
- [ ] Oracle account credentials saved
- [ ] Database credentials documented

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 9: Final Testing (5 minutes)

### Complete Application Test:

**As Admin:**
- [ ] Login as admin
- [ ] Navigate to dashboard
- [ ] Check students list
- [ ] Check companies section
- [ ] Test any CRUD operations
- [ ] Logout

**As Student:**
- [ ] Register new student account
- [ ] Check email for verification (if configured)
- [ ] Login as student
- [ ] View student dashboard
- [ ] Test student features
- [ ] Logout

**Performance:**
- [ ] Homepage loads in <3 seconds
- [ ] Dashboard loads quickly
- [ ] No console errors (F12 → Console)
- [ ] No 404 errors for assets
- [ ] Navigation works smoothly

**Mobile Test:**
- [ ] Open on mobile browser
- [ ] Check responsive design
- [ ] Test navigation
- [ ] Test login functionality

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## Phase 10: Ongoing Maintenance Setup (5 minutes)

### Monitoring:
- [ ] Sign up for UptimeRobot (free)
- [ ] Add monitor for `http://YOUR_IP/healthz`
- [ ] Set check interval: 5 minutes
- [ ] Add email alert
- [ ] Test alert works

### Backup Plan:
- [ ] Document backup strategy
- [ ] Note: Supabase auto-backs up database
- [ ] Consider code backup on GitHub
- [ ] Document recovery procedure

### Update Schedule:
- [ ] Plan weekly update check
- [ ] Subscribe to Laravel security alerts
- [ ] Document update procedure
- [ ] Test deployment script works

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🎉 Deployment Complete!

### Final Checklist:

- [ ] Server is running
- [ ] All services active
- [ ] Application accessible via browser
- [ ] Admin can login
- [ ] Students can register/login
- [ ] RAG service responding
- [ ] No errors in logs
- [ ] Performance acceptable
- [ ] Security measures applied
- [ ] Monitoring configured
- [ ] Documentation saved
- [ ] Backup plan ready

---

## 📊 Deployment Summary

**Fill in after completion:**

```
Deployment Date: _______________
Total Time Taken: _______________
Public IP: _______________
Domain (if any): _______________
SSL Enabled: Yes / No
Monitoring Setup: Yes / No
Any Issues Faced: _______________
___________________________________
___________________________________
```

---

## 🆘 Troubleshooting Checklist

### If Something Goes Wrong:

**502 Bad Gateway:**
- [ ] Check PHP-FPM: `sudo systemctl status php8.2-fpm`
- [ ] Restart: `sudo systemctl restart php8.2-fpm`
- [ ] Check Nginx logs

**Permission Errors:**
- [ ] Fix storage: `sudo chown -R www-data:www-data storage bootstrap/cache`
- [ ] Fix permissions: `sudo chmod -R 775 storage bootstrap/cache`

**Database Connection Failed:**
- [ ] Check .env DB settings
- [ ] Test connection: `php artisan tinker` then `DB::connection()->getPdo();`
- [ ] Verify Supabase credentials

**Assets Not Loading:**
- [ ] Verify public/build exists
- [ ] Re-run: `npm run build`
- [ ] Check Nginx asset serving

**RAG Service Down:**
- [ ] Check: `sudo supervisorctl status rag-service`
- [ ] View logs: `sudo tail -f /var/log/supervisor/rag-service.log`
- [ ] Restart: `sudo supervisorctl restart rag-service`

**Out of Memory:**
- [ ] Check: `free -h`
- [ ] Add swap space (see guide)
- [ ] Consider optimizing services

---

## 📚 Reference Documents

- [ ] Read: `ORACLE_CLOUD_DEPLOYMENT_GUIDE.md` - Complete guide
- [ ] Read: `ORACLE_CLOUD_QUICK_START.md` - Quick reference
- [ ] Read: `FREE_HOSTING_COMPARISON.md` - Why Oracle Cloud
- [ ] Keep: `oracle-setup.sh` - Automated setup script
- [ ] Use: `deploy.sh` - Deployment updates script
- [ ] Use: `check-services.sh` - Health check script

---

## ✅ Sign Off

**Deployment performed by:** _______________

**Date:** _______________

**Verified by:** _______________

**Status:** 🟢 Success | 🟡 Partial | 🔴 Failed

**Notes:**
```
_____________________________________________
_____________________________________________
_____________________________________________
```

---

**Congratulations! Your College Placement Portal is now live on Oracle Cloud Free Tier!** 🎉

**Access:** http://YOUR_PUBLIC_IP

**Monthly Cost:** $0 💰

**Next:** Share the URL with your users!

