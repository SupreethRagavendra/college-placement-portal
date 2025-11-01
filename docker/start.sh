#!/bin/bash
set -e

echo "🚀 Starting Laravel application..."

# Create .env file from environment variables
echo "📝 Creating .env file from environment variables..."
cat > /var/www/html/.env << EOF
APP_NAME="${APP_NAME:-Laravel}"
APP_ENV="${APP_ENV:-production}"
APP_KEY="${APP_KEY}"
APP_DEBUG="${APP_DEBUG:-false}"
APP_URL="${APP_URL:-http://localhost}"

LOG_CHANNEL="${LOG_CHANNEL:-stack}"
LOG_LEVEL="${LOG_LEVEL:-info}"

DB_CONNECTION="${DB_CONNECTION:-pgsql}"
DB_HOST="${DB_HOST:-db.wkqbukidxmzbgwauncrl.supabase.co}"
DB_PORT="${DB_PORT:-5432}"
DB_DATABASE="${DB_DATABASE:-postgres}"
DB_USERNAME="${DB_USERNAME:-postgres}"
DB_PASSWORD="${DB_PASSWORD}"
DB_SSLMODE="${DB_SSLMODE:-require}"

BROADCAST_DRIVER=log
CACHE_DRIVER=file
CACHE_STORE=file
FILESYSTEM_DISK=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=cookie
SESSION_LIFETIME=120
SESSION_SECURE_COOKIE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax
TRUSTED_PROXIES=*

MEMCACHED_HOST=127.0.0.1

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="\${APP_NAME}"
EOF

echo "✅ .env file created"

# Use environment variables for database connection
echo "📝 Using database connection from environment"
echo "📍 DB_HOST: $DB_HOST"
echo "📍 DB_PORT: $DB_PORT"
echo "📍 DB_USERNAME: $DB_USERNAME"
echo "📍 DB_SSLMODE: $DB_SSLMODE"

# Test database connection (quick check only)
echo "⏳ Testing database connection..."
# Force IPv4 by resolving hostname to IPv4 address
DB_HOST_IPV4=$(getent ahostsv4 "${DB_HOST}" | head -1 | awk '{print $1}' || echo "${DB_HOST}")
echo "📍 Resolved DB_HOST to IPv4: $DB_HOST_IPV4"

if php -r "
try {
    \$pdo = new PDO(
        'pgsql:host=${DB_HOST_IPV4};port=${DB_PORT};dbname=${DB_DATABASE};sslmode=${DB_SSLMODE}',
        '${DB_USERNAME}',
        '${DB_PASSWORD}',
        [PDO::ATTR_TIMEOUT => 10, PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    echo 'connected';
    exit(0);
} catch (Exception \$e) {
    echo 'Error: ' . \$e->getMessage();
    exit(1);
}
" 2>&1 | grep -q "connected"; then
    echo "✅ Database connection established"
    DB_CONNECTED=true
else
    echo "⚠️  Could not connect to database, but continuing..."
    echo "⚠️  Laravel will handle database connections"
    DB_CONNECTED=false
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

# Run database migrations
echo "🗄️  Running database migrations..."
php artisan migrate --force --no-interaction || {
    echo "⚠️  Migration failed - database may not be available yet"
    echo "⚠️  Application will continue, but some features may not work"
}

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

# Update Nginx to use Render's PORT (defaults to 8000 if not set)
PORT=${PORT:-8000}
echo "🌐 Configuring Nginx to listen on port $PORT..."
sed -i "s/listen 8000;/listen $PORT;/g" /etc/nginx/http.d/default.conf
sed -i "s/listen \[::\]:8000;/listen [::]:$PORT;/g" /etc/nginx/http.d/default.conf

echo "🌐 Starting Nginx and PHP-FPM..."

# Start supervisor (which manages nginx and php-fpm)
exec /usr/bin/supervisord -c /etc/supervisord.conf
