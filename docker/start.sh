#!/bin/bash
set -e

echo "🚀 Starting Laravel application..."

# Use environment variables for database connection
echo "📝 Using database connection from environment"
echo "📍 DB_HOST: $DB_HOST"
echo "📍 DB_PORT: $DB_PORT"
echo "📍 DB_USERNAME: $DB_USERNAME"
echo "📍 DB_SSLMODE: $DB_SSLMODE"

# Test database connection with better error handling
echo "⏳ Testing database connection..."
MAX_RETRIES=10
RETRY_COUNT=0
DB_CONNECTED=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$DB_CONNECTED" = "false" ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Connection attempt $RETRY_COUNT/$MAX_RETRIES..."
    
    # Try to connect using pg_isready first (if available)
    if command -v pg_isready &> /dev/null; then
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -t 5 2>/dev/null; then
            DB_CONNECTED=true
            echo "✅ PostgreSQL server is ready"
        fi
    fi
    
    # Fallback to PHP connection test
    if [ "$DB_CONNECTED" = "false" ]; then
        if php -r "try { \$pdo = new PDO('pgsql:host=${DB_HOST};port=${DB_PORT};dbname=${DB_DATABASE};sslmode=${DB_SSLMODE}', '${DB_USERNAME}', '${DB_PASSWORD}'); echo 'connected'; } catch (Exception \$e) { exit(1); }" 2>/dev/null | grep -q "connected"; then
            DB_CONNECTED=true
            echo "✅ Database connection established via PHP"
        fi
    fi
    
    if [ "$DB_CONNECTED" = "false" ]; then
        echo "⏳ Waiting 5 seconds before retry..."
        sleep 5
    fi
done

if [ "$DB_CONNECTED" = "false" ]; then
    echo "⚠️  Could not establish database connection after $MAX_RETRIES attempts"
    echo "⚠️  Proceeding with application startup anyway..."
    echo "⚠️  Database operations may fail until connection is restored"
else
    echo "✅ Database connection verified"
fi

# Generate APP_KEY if not set
if [ -z "$APP_KEY" ] || [ "$APP_KEY" = "base64:" ]; then
    echo "🔑 Generating APP_KEY..."
    php artisan key:generate --force
    echo "⚠️  IMPORTANT: Save the generated APP_KEY to your Render environment variables!"
else
    echo "✅ APP_KEY is set"
fi

# Clear all caches
echo "🧹 Clearing caches..."
php artisan config:clear
php artisan cache:clear
php artisan view:clear
php artisan route:clear

# Ensure storage directories have proper permissions before migrations
echo "🔐 Setting storage permissions..."
chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Run database migrations only if connected
if [ "$DB_CONNECTED" = "true" ]; then
    echo "🗄️  Running database migrations..."
    php artisan migrate --force --no-interaction || {
        echo "⚠️  Migration failed - will retry on next deployment"
    }
else
    echo "⚠️  Skipping migrations - database not available"
fi

# Cache only routes and views, NOT config (to allow runtime env vars for sessions)
echo "⚡ Caching routes and views..."
php artisan route:cache || echo "⚠️  Route caching failed - continuing..."
php artisan view:cache || echo "⚠️  View caching failed - continuing..."

# Create storage link
echo "🔗 Creating storage link..."
php artisan storage:link || true

# Final permission check
echo "🔐 Final permission check..."
chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Test session functionality
echo "🧪 Testing session functionality..."
php -r "
try {
    session_start();
    \$_SESSION['test'] = 'working';
    echo '✅ Session test passed';
} catch (Exception \$e) {
    echo '⚠️  Session test failed: ' . \$e->getMessage();
}
" || echo "⚠️  Session test encountered an error"

echo "✅ Laravel application ready!"
echo "🌐 Starting Nginx and PHP-FPM..."

# Start supervisor (which manages nginx and php-fpm)
exec /usr/bin/supervisord -c /etc/supervisord.conf
