#!/usr/bin/env bash
# Render.com Build Script for Laravel Application

set -e  # Exit on error

echo "🚀 Starting Render build process..."

# 1. Create necessary storage directories
echo "📁 Creating storage directories..."
mkdir -p storage/framework/cache/data
mkdir -p storage/framework/sessions
mkdir -p storage/framework/views
mkdir -p storage/logs
mkdir -p bootstrap/cache

# 2. Set proper permissions
echo "🔐 Setting permissions..."
chmod -R 775 storage bootstrap/cache
# Ensure session directory exists and is writable
mkdir -p storage/framework/sessions
chmod -R 777 storage/framework/sessions

# 3. Install PHP dependencies
echo "📦 Installing PHP dependencies..."
composer install --no-dev --optimize-autoloader --no-interaction --prefer-dist

# 4. Clear any existing caches
echo "🧹 Clearing caches..."
php artisan config:clear || true
php artisan cache:clear || true
php artisan view:clear || true
php artisan route:clear || true

# 5. Generate application key if not exists
echo "🔑 Checking application key..."
if [ -z "$APP_KEY" ] || [ "$APP_KEY" = "base64:" ]; then
    echo "⚠️  APP_KEY not set or empty, generating new key..."
    # Generate a key and export it for the current session
    php artisan key:generate --force --no-interaction
    echo "✅ New APP_KEY generated"
    echo "⚠️  IMPORTANT: This key is now set. Do not regenerate in production!"
else
    echo "✅ APP_KEY already set"
fi

# Test if key works
echo "🔍 Verifying APP_KEY..."
if php artisan config:show app.key | grep -q "base64:"; then
    echo "✅ APP_KEY is valid"
else
    echo "⚠️  APP_KEY might be invalid, regenerating..."
    php artisan key:generate --force --no-interaction
fi

# 6. Install Node dependencies and build assets
echo "🎨 Building frontend assets..."
npm ci --prefer-offline --no-audit
npm run build

# 7. Run database migrations
echo "🗄️ Running database migrations..."
php artisan migrate --force --no-interaction

# 7.5. Seed admin user
echo "👤 Seeding admin user..."
php artisan db:seed --class=AdminSeeder --force --no-interaction || echo "⚠️  Seeder already ran or failed, continuing..."

# 8. Cache routes and views only (NOT config to allow runtime env vars)
echo "⚡ Caching routes and views..."
php artisan route:cache
php artisan view:cache
echo "⚠️  Skipping config:cache to allow runtime environment variables"

# 9. Create symbolic link for storage (if needed)
echo "🔗 Creating storage link..."
php artisan storage:link || true

echo "✅ Build completed successfully!"
