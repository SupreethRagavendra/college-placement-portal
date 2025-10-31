#!/usr/bin/env bash
# Diagnostic script for Render deployment issues

echo "================================"
echo "🔍 Render Deployment Diagnostics"
echo "================================"
echo ""

# Check PHP version
echo "📌 PHP Version:"
php -v
echo ""

# Check if .env exists
echo "📌 Environment File:"
if [ -f .env ]; then
    echo "✅ .env file exists"
else
    echo "❌ .env file missing"
fi
echo ""

# Check APP_KEY
echo "📌 APP_KEY Status:"
if [ -z "$APP_KEY" ]; then
    echo "❌ APP_KEY is not set"
else
    echo "✅ APP_KEY is set: ${APP_KEY:0:20}..."
fi
echo ""

# Check database connection
echo "📌 Database Configuration:"
echo "DB_CONNECTION: $DB_CONNECTION"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_DATABASE: $DB_DATABASE"
echo "DB_USERNAME: $DB_USERNAME"
echo ""

# Check storage directories
echo "📌 Storage Directories:"
for dir in storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
        ls -la "$dir" | head -n 3
    else
        echo "❌ $dir missing"
    fi
done
echo ""

# Check permissions
echo "📌 Permissions:"
ls -la storage/ | head -n 5
echo ""

# Test database connection
echo "📌 Testing Database Connection:"
php artisan tinker --execute="try { DB::connection()->getPdo(); echo 'Database connection: SUCCESS'; } catch (Exception \$e) { echo 'Database connection: FAILED - ' . \$e->getMessage(); }"
echo ""

# Check if vendor exists
echo "📌 Vendor Directory:"
if [ -d vendor ]; then
    echo "✅ vendor directory exists"
else
    echo "❌ vendor directory missing"
fi
echo ""

# Check if node_modules exists
echo "📌 Node Modules:"
if [ -d node_modules ]; then
    echo "✅ node_modules directory exists"
else
    echo "❌ node_modules directory missing"
fi
echo ""

# Check public/build
echo "📌 Built Assets:"
if [ -d public/build ]; then
    echo "✅ public/build directory exists"
    ls -la public/build | head -n 5
else
    echo "❌ public/build directory missing"
fi
echo ""

# List environment variables (sanitized)
echo "📌 Environment Variables:"
echo "APP_ENV: $APP_ENV"
echo "APP_DEBUG: $APP_DEBUG"
echo "APP_URL: $APP_URL"
echo "LOG_CHANNEL: $LOG_CHANNEL"
echo "LOG_LEVEL: $LOG_LEVEL"
echo "CACHE_DRIVER: $CACHE_DRIVER"
echo "SESSION_DRIVER: $SESSION_DRIVER"
echo ""

echo "================================"
echo "✅ Diagnostics Complete"
echo "================================"
