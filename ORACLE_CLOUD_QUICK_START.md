# ⚡ Oracle Cloud - Quick Start (5 Steps)

## 🚀 Deploy in 60 Minutes

---

## Step 1: Create Oracle Account (10 min)
1. Go to: https://www.oracle.com/cloud/free/
2. Sign up (email + phone verification)
3. Choose region: **Mumbai** or **Singapore**
4. **No credit card required!**

---

## Step 2: Create VM Instance (5 min)

**Quick Settings:**
```
Name: college-placement-portal
Image: Ubuntu 22.04
Shape: VM.Standard.E2.1.Micro (Always Free)
RAM: 1GB
Storage: 50GB
Public IP: ✅ Yes
```

1. Download SSH key → Save as `oracle-key.pem`
2. Note your **Public IP address**
3. Open firewall ports: 80, 443, 8001

---

## Step 3: Connect & Run Setup Script (40 min)

### Connect:
```bash
# Windows PowerShell:
ssh -i "D:\path\to\oracle-key.pem" ubuntu@YOUR_PUBLIC_IP

# Linux/Mac:
chmod 400 oracle-key.pem
ssh -i oracle-key.pem ubuntu@YOUR_PUBLIC_IP
```

### Run Automated Setup:
```bash
# Download and run setup script
curl -o setup.sh https://raw.githubusercontent.com/YOUR_USERNAME/college-placement-portal/main/oracle-setup.sh
chmod +x setup.sh
./setup.sh
```

**Or manual setup:** Follow [ORACLE_CLOUD_DEPLOYMENT_GUIDE.md](./ORACLE_CLOUD_DEPLOYMENT_GUIDE.md)

---

## Step 4: Configure Your Project (5 min)

```bash
cd /var/www/college-placement-portal

# Edit environment
nano .env

# Update:
# - APP_URL (your public IP)
# - DB credentials (Supabase)
# - Mail settings (if needed)

# Generate key
php artisan key:generate

# Run migrations
php artisan migrate --force

# Seed admin
php artisan db:seed --class=AdminSeeder --force
```

---

## Step 5: Start Services (2 min)

```bash
# Start everything
sudo systemctl restart nginx php8.2-fpm
sudo supervisorctl restart rag-service

# Check status
sudo systemctl status nginx
sudo supervisorctl status rag-service
```

---

## ✅ Done!

**Access your application:**
- URL: `http://YOUR_PUBLIC_IP`
- Admin: admin@portal.com / Admin@123

---

## 🔧 Common Commands

```bash
# View logs
sudo tail -f /var/log/nginx/college-portal-error.log

# Restart services
sudo systemctl restart nginx php8.2-fpm
sudo supervisorctl restart rag-service

# Deploy updates
cd /var/www/college-placement-portal
git pull
./deploy.sh
```

---

## 🆘 Troubleshooting

**Can't connect?**
```bash
# Check Oracle firewall (Security List)
# Check Ubuntu firewall
sudo iptables -L
```

**502 Bad Gateway?**
```bash
sudo systemctl restart php8.2-fpm
```

**Permission errors?**
```bash
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

---

## 📊 What You Get FREE Forever

✅ 1GB RAM server (24/7)
✅ 50GB storage
✅ 10TB monthly transfer
✅ Public IP address
✅ **Cost: $0/month**

---

**Full Guide**: [ORACLE_CLOUD_DEPLOYMENT_GUIDE.md](./ORACLE_CLOUD_DEPLOYMENT_GUIDE.md)

