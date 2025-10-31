#!/bin/bash
# ================================================================
# Production Optimization Script for College Placement Portal
# ================================================================
# This script optimizes Laravel for production deployment
# Run this AFTER deploying to production server
# ================================================================

echo ""
echo "============================================================"
echo "   COLLEGE PLACEMENT PORTAL - PRODUCTION OPTIMIZATION"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "⚠️  Warning: Running as root. Consider running as www-data user."
   echo ""
fi

# 1. Clear all caches first
echo "[1/9] Clearing existing caches..."
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
php artisan event:clear
echo "✓ Caches cleared"
echo ""

# 2. Set proper permissions
echo "[2/9] Setting proper permissions..."
chmod -R 755 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache 2>/dev/null || true
echo "✓ Permissions set"
echo ""

# 3. Optimize Composer autoloader
echo "[3/9] Optimizing Composer autoloader..."
composer install --optimize-autoloader --no-dev --no-interaction
echo "✓ Autoloader optimized"
echo ""

# 4. Cache configuration
echo "[4/9] Caching configuration..."
php artisan config:cache
echo "✓ Configuration cached"
echo ""

# 5. Cache routes
echo "[5/9] Caching routes..."
php artisan route:cache
echo "✓ Routes cached"
echo ""

# 6. Cache views
echo "[6/9] Caching views..."
php artisan view:cache
echo "✓ Views cached"
echo ""

# 7. Cache events
echo "[7/9] Caching events..."
php artisan event:cache
echo "✓ Events cached"
echo ""

# 8. Build frontend assets for production
echo "[8/9] Building optimized frontend assets..."
if command -v npm &> /dev/null; then
    npm ci --production
    npm run build
    echo "✓ Frontend assets built"
else
    echo "⚠️  npm not found. Please build assets manually with 'npm run build'"
fi
echo ""

# 9. Run database migrations (if needed)
echo "[9/9] Running database migrations..."
php artisan migrate --force
echo "✓ Migrations completed"
echo ""

echo ""
echo "============================================================"
echo "   OPTIMIZATION COMPLETE!"
echo "============================================================"
echo ""
echo "Your application is now optimized for production."
echo ""
echo "IMPORTANT NOTES:"
echo "- Make sure APP_ENV=production in .env"
echo "- Make sure APP_DEBUG=false in .env"
echo "- Enable OPcache in php.ini for maximum performance"
echo "- Consider using Redis/Memcached for cache driver"
echo "- Use queue workers for background jobs"
echo ""
echo "To start queue worker:"
echo "  php artisan queue:work --daemon"
echo ""
echo "To restart PHP-FPM (if using):"
echo "  sudo systemctl restart php8.2-fpm"
echo ""
echo "To restart web server:"
echo "  sudo systemctl restart nginx  # or apache2"
echo ""
echo "============================================================"

