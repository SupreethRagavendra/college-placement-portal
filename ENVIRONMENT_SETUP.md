# 🔧 Environment Setup Guide for Render Deployment

This guide provides detailed instructions for setting up environment variables and database configuration for your College Placement Portal on Render.

## 📋 Required Environment Variables

### 1. Application Configuration

```env
# Application Settings
APP_NAME="College Placement Portal"
APP_ENV=production
APP_KEY=base64:your-generated-app-key-here
APP_DEBUG=false
APP_URL=https://your-app-name.onrender.com

# Logging
LOG_CHANNEL=stderr
LOG_LEVEL=error
```

**How to generate APP_KEY:**
```bash
php artisan key:generate --show
```

### 2. Database Configuration (Supabase PostgreSQL)

```env
# Database Settings
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD="Supreeeth24#"
DB_SSLMODE=require
```

**Important Notes:**
- Your Supabase database is already configured
- SSL mode is required for Supabase connections
- The database credentials are already set up in your project

### 3. Email Configuration

Choose one of the following email service configurations:

#### Option A: Gmail SMTP (Free)

```env
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS="your-email@gmail.com"
MAIL_FROM_NAME="${APP_NAME}"
```

**Gmail Setup Steps:**
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → 2-Step Verification → App passwords
3. Generate an app password for "Mail"
4. Use this 16-character password (not your regular Gmail password)

#### Option B: SendGrid (Recommended for Production)

```env
MAIL_MAILER=smtp
MAIL_HOST=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS="noreply@yourdomain.com"
MAIL_FROM_NAME="${APP_NAME}"
```

**SendGrid Setup Steps:**
1. Sign up for SendGrid (free tier: 100 emails/day)
2. Create an API key in SendGrid dashboard
3. Verify your sender identity
4. Use the API key as MAIL_PASSWORD

#### Option C: Mailgun (Alternative)

```env
MAIL_MAILER=smtp
MAIL_HOST=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=your-mailgun-smtp-username
MAIL_PASSWORD=your-mailgun-smtp-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS="noreply@yourdomain.com"
MAIL_FROM_NAME="${APP_NAME}"
```

### 4. Cache and Session Configuration

```env
# Cache and Session
CACHE_DRIVER=file
SESSION_DRIVER=file
SESSION_LIFETIME=120
QUEUE_CONNECTION=sync
```

### 5. File Storage Configuration

```env
# File Storage
FILESYSTEM_DISK=local
```

## 🚀 Setting Up Environment Variables in Render

### Method 1: Using Render Dashboard

1. **Go to your service dashboard** in Render
2. **Click on "Environment"** tab
3. **Add each environment variable** one by one:

| Key | Value | Description |
|-----|-------|-------------|
| `APP_NAME` | `College Placement Portal` | Application name |
| `APP_ENV` | `production` | Environment type |
| `APP_KEY` | `base64:...` | Generated app key |
| `APP_DEBUG` | `false` | Debug mode |
| `APP_URL` | `https://your-app.onrender.com` | Your Render URL |
| `DB_CONNECTION` | `pgsql` | Database type |
| `DB_HOST` | `db.wkqbukidxmzbgwauncrl.supabase.co` | Supabase host |
| `DB_PORT` | `5432` | Database port |
| `DB_DATABASE` | `postgres` | Database name |
| `DB_USERNAME` | `postgres` | Database username |
| `DB_PASSWORD` | `Supreeeth24#` | Database password |
| `DB_SSLMODE` | `require` | SSL requirement |
| `MAIL_MAILER` | `smtp` | Mail driver |
| `MAIL_HOST` | `smtp.gmail.com` | SMTP host |
| `MAIL_PORT` | `587` | SMTP port |
| `MAIL_USERNAME` | `your-email@gmail.com` | Your email |
| `MAIL_PASSWORD` | `your-app-password` | App password |
| `MAIL_ENCRYPTION` | `tls` | Encryption type |
| `MAIL_FROM_ADDRESS` | `your-email@gmail.com` | From address |
| `MAIL_FROM_NAME` | `${APP_NAME}` | From name |
| `LOG_CHANNEL` | `stderr` | Log output |
| `CACHE_DRIVER` | `file` | Cache driver |
| `SESSION_DRIVER` | `file` | Session driver |
| `QUEUE_CONNECTION` | `sync` | Queue driver |

### Method 2: Using render.yaml (Recommended)

If you're using the `render.yaml` file, add environment variables there:

```yaml
services:
  - type: web
    name: college-placement-portal
    env: php
    plan: free
    buildCommand: |
      composer install --no-dev --optimize-autoloader
      php artisan key:generate --force
      php artisan config:cache
      php artisan route:cache
      php artisan view:cache
      npm ci
      npm run build
    startCommand: php artisan serve --host=0.0.0.0 --port=$PORT
    envVars:
      - key: APP_NAME
        value: "College Placement Portal"
      - key: APP_ENV
        value: production
      - key: APP_DEBUG
        value: false
      - key: LOG_CHANNEL
        value: stderr
      - key: DB_CONNECTION
        value: pgsql
      - key: DB_HOST
        value: db.wkqbukidxmzbgwauncrl.supabase.co
      - key: DB_PORT
        value: 5432
      - key: DB_DATABASE
        value: postgres
      - key: DB_USERNAME
        value: postgres
      - key: DB_PASSWORD
        value: "Supreeeth24#"
      - key: DB_SSLMODE
        value: require
      - key: MAIL_MAILER
        value: smtp
      - key: MAIL_HOST
        value: smtp.gmail.com
      - key: MAIL_PORT
        value: 587
      - key: MAIL_USERNAME
        value: your-email@gmail.com
      - key: MAIL_PASSWORD
        value: your-app-password
      - key: MAIL_ENCRYPTION
        value: tls
      - key: MAIL_FROM_ADDRESS
        value: your-email@gmail.com
      - key: MAIL_FROM_NAME
        value: "${APP_NAME}"
      - key: CACHE_DRIVER
        value: file
      - key: SESSION_DRIVER
        value: file
      - key: QUEUE_CONNECTION
        value: sync
```

## 🗄️ Database Setup

### 1. Verify Database Connection

Your Supabase PostgreSQL database is already configured with:
- **Host**: `db.wkqbukidxmzbgwauncrl.supabase.co`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `Supreeeth24#`
- **SSL Mode**: `require`

### 2. Run Database Migrations

After deployment, run these commands in Render Shell:

```bash
# Run migrations
php artisan migrate --force

# Seed the database with admin user
php artisan db:seed --class=AdminSeeder --force
```

### 3. Verify Database Tables

Check if all tables are created:

```bash
php artisan tinker
# Then run:
DB::select('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\';');
```

## 📧 Email Service Setup

### Gmail SMTP Setup (Recommended for Testing)

1. **Enable 2FA on Gmail**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate App Password**:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app
   - Copy the 16-character password

3. **Configure Environment Variables**:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-character-app-password
   MAIL_FROM_ADDRESS=your-email@gmail.com
   ```

### SendGrid Setup (Recommended for Production)

1. **Sign up for SendGrid**:
   - Go to [SendGrid](https://sendgrid.com)
   - Create a free account (100 emails/day)

2. **Create API Key**:
   - Go to Settings → API Keys
   - Create a new API key with "Mail Send" permissions
   - Copy the API key

3. **Verify Sender Identity**:
   - Go to Settings → Sender Authentication
   - Verify your domain or single sender

4. **Configure Environment Variables**:
   ```env
   MAIL_HOST=smtp.sendgrid.net
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=your-sendgrid-api-key
   MAIL_FROM_ADDRESS=noreply@yourdomain.com
   ```

## 🧪 Testing Your Configuration

### 1. Test Database Connection

```bash
php artisan tinker
# Then run:
DB::connection()->getPdo();
```

### 2. Test Email Configuration

```bash
php artisan tinker
# Then run:
Mail::raw('Test email from Render', function($message) {
    $message->to('test@example.com')->subject('Test Email');
});
```

### 3. Test Application

1. Visit your Render URL
2. Try to register a new account
3. Check if verification email is sent
4. Complete the registration process
5. Test login functionality

## 🚨 Common Issues and Solutions

### Database Connection Issues

**Error**: `Connection could not be established`

**Solutions**:
- Verify DB_HOST is correct
- Check DB_SSLMODE is set to `require`
- Ensure database credentials are correct
- Check if Supabase database is active

### Email Issues

**Error**: `Connection could not be established with host`

**Solutions**:
- Verify SMTP credentials
- Use app password for Gmail (not regular password)
- Check if 2FA is enabled for Gmail
- Try different SMTP service (SendGrid, Mailgun)

### Application Key Issues

**Error**: `No application encryption key has been specified`

**Solutions**:
- Generate new APP_KEY: `php artisan key:generate --show`
- Add APP_KEY to environment variables
- Redeploy the application

### Asset Loading Issues

**Error**: CSS/JS files not loading

**Solutions**:
- Ensure `npm run build` completes successfully
- Check if build files are in `public/build/`
- Verify file permissions
- Clear browser cache

## 📊 Environment Variables Checklist

- [ ] APP_NAME set to "College Placement Portal"
- [ ] APP_ENV set to "production"
- [ ] APP_KEY generated and set
- [ ] APP_DEBUG set to "false"
- [ ] APP_URL set to your Render URL
- [ ] Database credentials configured
- [ ] Email service configured
- [ ] Log channel set to "stderr"
- [ ] Cache and session drivers set
- [ ] All required variables added to Render

## 🔒 Security Considerations

1. **Never commit .env files** to version control
2. **Use strong passwords** for all services
3. **Enable 2FA** on all accounts
4. **Regularly rotate API keys** and passwords
5. **Monitor access logs** for suspicious activity
6. **Use HTTPS** for all communications
7. **Keep dependencies updated**

---

**Next Steps**: After setting up environment variables, proceed to the deployment process outlined in `RENDER_DEPLOYMENT.md`.
