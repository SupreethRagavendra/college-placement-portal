#!/bin/bash

# Render Deployment Script for College Placement Portal
# This script helps with the deployment process

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "artisan" ]; then
    echo "❌ Error: artisan file not found. Please run this script from the Laravel project root."
    exit 1
fi

# Install dependencies
echo "📦 Installing PHP dependencies..."
composer install --no-dev --optimize-autoloader

# Install Node dependencies and build assets
echo "🎨 Installing Node dependencies and building assets..."
npm ci
npm run build

# Generate application key if not exists
if [ -z "$APP_KEY" ]; then
    echo "🔑 Generating application key..."
    php artisan key:generate --force
fi

# Cache configuration
echo "⚡ Caching configuration..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Run migrations (only if not in production or if explicitly requested)
if [ "$APP_ENV" != "production" ] || [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "🗄️ Running database migrations..."
    php artisan migrate --force
    
    echo "🌱 Seeding database..."
    php artisan db:seed --class=AdminSeeder --force
fi

# Set proper permissions
echo "🔐 Setting permissions..."
chmod -R 755 storage
chmod -R 755 bootstrap/cache

echo "✅ Deployment process completed!"
echo "🌐 Your application should now be running on Render."
