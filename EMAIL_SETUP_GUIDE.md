# 📧 Email Configuration Guide for College Placement Portal

## Overview

The College Placement Portal uses email notifications to communicate with students about their account status (approved/rejected). This guide explains how to configure email settings properly.

## ✅ Email Configuration Fixed

### Changes Made:

1. **Fixed "From" Display Name**
   - Email will now show as "College Placement Portal" (or your custom name)
   - Not as the raw email address (e.g., "aromaticrootq@gmail.com")
   - Configured via `MAIL_FROM_NAME` in `.env` file

2. **Updated Email Content**
   - Changed from "job posting/searching" to "training and assessments"
   - Focused on:
     - Skill assessments
     - AI chatbot assistance
     - Training and preparation
     - Progress tracking
   - Not focused on job applications

3. **Proper SMTP Configuration**
   - Changed default from 'log' to 'smtp'
   - Added encryption support (TLS)
   - Uses environment variables for credentials

## 🔧 How to Configure Email

### Step 1: Set Up Your Email Service

Choose one of the following email services:

#### Option A: Gmail (Recommended for Development)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Select "Mail" and generate password
   - Copy the 16-character password

3. **Update `.env` file:**
   ```env
   MAIL_MAILER=smtp
   MAIL_HOST=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-character-app-password
   MAIL_ENCRYPTION=tls
   MAIL_FROM_ADDRESS=your-email@gmail.com
   MAIL_FROM_NAME="College Placement Portal"
   ```

#### Option B: SendGrid (Recommended for Production)

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key in your dashboard
3. Verify your sender identity

4. **Update `.env` file:**
   ```env
   MAIL_MAILER=smtp
   MAIL_HOST=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=your-sendgrid-api-key
   MAIL_ENCRYPTION=tls
   MAIL_FROM_ADDRESS=noreply@yourdomain.com
   MAIL_FROM_NAME="College Placement Portal"
   ```

#### Option C: Mailgun (Alternative)

1. Sign up at [Mailgun](https://www.mailgun.com/)
2. Get your SMTP credentials
3. Verify your domain

4. **Update `.env` file:**
   ```env
   MAIL_MAILER=smtp
   MAIL_HOST=smtp.mailgun.org
   MAIL_PORT=587
   MAIL_USERNAME=your-mailgun-smtp-username
   MAIL_PASSWORD=your-mailgun-smtp-password
   MAIL_ENCRYPTION=tls
   MAIL_FROM_ADDRESS=noreply@yourdomain.com
   MAIL_FROM_NAME="College Placement Portal"
   ```

### Step 2: Test Email Configuration

Run the test command:

```bash
php artisan test:email your-test-email@gmail.com approved
```

For rejection email test:

```bash
php artisan test:email your-test-email@gmail.com rejected
```

### Step 3: Check Logs

If emails aren't sending, check the logs:

```bash
# Windows
type storage\logs\laravel.log | findstr /i "email"

# Linux/Mac
tail -f storage/logs/laravel.log | grep -i email
```

## 📬 Email Templates

### Approval Email Features:
- ✅ Welcome message
- ✅ Portal access instructions
- ✅ Training features overview:
  - Skill assessments
  - AI chatbot
  - Progress tracking
  - Placement preparation
- ✅ Support contact info from `.env`

### Rejection Email Features:
- ℹ️ Polite rejection notice
- ℹ️ Reason for rejection (if provided)
- ℹ️ Steps to reapply
- ℹ️ Support contact info from `.env`

## 🎯 Important Notes

### Email Display Name
The email will display as:
```
From: College Placement Portal <your-email@gmail.com>
```
NOT as:
```
From: your-email@gmail.com
```

This is controlled by `MAIL_FROM_NAME` in your `.env` file.

### Portal Purpose
Emails now correctly describe the portal as a **training and assessment platform**, not a job posting site:

- ✅ Take assessments
- ✅ Use AI chatbot
- ✅ Track progress
- ✅ Prepare for placements

- ❌ Browse job postings
- ❌ Apply for positions
- ❌ Search for jobs

### Environment Variables Used

All email content dynamically uses:
- `MAIL_FROM_ADDRESS` - Support email address
- `MAIL_FROM_NAME` - Display name (e.g., "College Placement Portal")
- `APP_URL` - Portal URL for login links
- `APP_NAME` - Application name

## 🔍 Troubleshooting

### Problem: Emails not sending

**Solution:**
1. Check `.env` configuration
2. Run: `php artisan config:clear`
3. Run: `php artisan cache:clear`
4. Check logs: `storage/logs/laravel.log`
5. Test with: `php artisan test:email your-email@gmail.com approved`

### Problem: "From" shows email address instead of name

**Solution:**
1. Ensure `MAIL_FROM_NAME` is set in `.env`
2. Clear config cache: `php artisan config:clear`
3. Restart your application

### Problem: Gmail rejects emails

**Solution:**
1. Enable 2-Factor Authentication
2. Use App Password (not regular password)
3. Enable "Less secure app access" (if using regular password)

### Problem: Emails go to spam

**Solution:**
1. Use a verified email service (SendGrid, Mailgun)
2. Set up SPF, DKIM, and DMARC records
3. Use a custom domain (not Gmail)
4. Don't send too many emails at once

## 📊 Email Flow

When admin approves/rejects a student:

1. Admin clicks "Approve" or "Reject" button
2. `AdminController` updates database
3. `EmailNotificationService` is called
4. Email is sent via `StudentStatusMail` mailable
5. Email uses proper template (`student-approved.blade.php` or `student-rejected.blade.php`)
6. Student receives email with proper "From" name
7. Log entry is created for tracking

## 🚀 Production Deployment

For production (e.g., Render, Heroku):

1. Set environment variables in hosting dashboard
2. Use SendGrid or Mailgun (not Gmail)
3. Set `MAIL_MAILER=smtp`
4. Set `APP_DEBUG=false`
5. Set `LOG_LEVEL=error`
6. Monitor email delivery in service dashboard

## 📞 Support

If you need help:
- Check logs: `storage/logs/laravel.log`
- Test email: `php artisan test:email your-email@gmail.com`
- Contact: Use the email configured in `MAIL_FROM_ADDRESS`

---

**Last Updated:** {{ date('Y-m-d') }}
**Version:** 1.0

