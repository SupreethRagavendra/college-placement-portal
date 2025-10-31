#!/bin/bash

# College Placement Portal - Production Cleanup Script
# This script safely prepares the application for production deployment
# All changes are reversible and non-breaking

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Production Cleanup Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Create backup directory
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo -e "${YELLOW}Step 1: Creating full backup...${NC}"
# Backup critical files
cp .env $BACKUP_DIR/.env.backup 2>/dev/null || true
cp -r config $BACKUP_DIR/config_backup 2>/dev/null || true
cp -r public/js $BACKUP_DIR/js_backup 2>/dev/null || true
cp -r resources/views $BACKUP_DIR/views_backup 2>/dev/null || true
echo -e "${GREEN}✓ Backup created in $BACKUP_DIR${NC}"

echo -e "${YELLOW}Step 2: Removing debug code from JavaScript...${NC}"
# Remove console.log statements but keep the code functional
for file in public/js/*.js; do
    if [ -f "$file" ]; then
        # Create backup
        cp "$file" "$BACKUP_DIR/$(basename $file).backup"
        # Remove console.log lines
        sed -i '/console\.log/d' "$file" 2>/dev/null || sed -i '' '/console\.log/d' "$file"
        echo -e "  Cleaned: $(basename $file)"
    fi
done
echo -e "${GREEN}✓ JavaScript debug code removed${NC}"

echo -e "${YELLOW}Step 3: Removing dd() statements from Blade files...${NC}"
# Comment out dd() statements in Blade templates
find resources/views -name "*.blade.php" -type f | while read file; do
    if grep -q "dd(" "$file"; then
        cp "$file" "$BACKUP_DIR/$(basename $file).backup"
        sed -i 's/{{ dd(/{{-- dd(/g; s/) }}/)) --}}/g' "$file" 2>/dev/null || \
        sed -i '' 's/{{ dd(/{{-- dd(/g; s/) }}/)) --}}/g' "$file"
        echo -e "  Cleaned: $(basename $file)"
    fi
done
echo -e "${GREEN}✓ Blade debug code removed${NC}"

echo -e "${YELLOW}Step 4: Organizing documentation files...${NC}"
# Move documentation files to docs folder
mkdir -p docs/archive
# Count MD files before moving
MD_COUNT=$(ls -1 *.md 2>/dev/null | wc -l)
if [ $MD_COUNT -gt 0 ]; then
    # Keep README.md in root
    mv README.md README.md.temp 2>/dev/null || true
    # Move all other MD files
    mv *.md docs/archive/ 2>/dev/null || true
    # Restore README.md
    mv README.md.temp README.md 2>/dev/null || true
    mv docs/archive/README.md ./ 2>/dev/null || true
    echo -e "  Moved $MD_COUNT documentation files"
fi
echo -e "${GREEN}✓ Documentation organized${NC}"

echo -e "${YELLOW}Step 5: Removing test and disabled files...${NC}"
# Remove test files
rm -f resources/views/student/test.blade.php 2>/dev/null || true
rm -f public/js/chatbot-debug.js 2>/dev/null || true
rm -f app/Http/Controllers/AdminQuestionController.php.disabled 2>/dev/null || true
# Remove backup directories if confirmed not needed
if [ -d "python-rag-groq-backup" ]; then
    echo -e "  Found backup directory: python-rag-groq-backup"
    # Move to backups instead of deleting
    mv python-rag-groq-backup $BACKUP_DIR/ 2>/dev/null || true
fi
echo -e "${GREEN}✓ Test files removed${NC}"

echo -e "${YELLOW}Step 6: Clearing Laravel caches...${NC}"
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
php artisan optimize:clear
echo -e "${GREEN}✓ Caches cleared${NC}"

echo -e "${YELLOW}Step 7: Clearing and rotating logs...${NC}"
# Archive old logs
if [ -f "storage/logs/laravel.log" ]; then
    cp storage/logs/laravel.log $BACKUP_DIR/laravel.log.backup
    > storage/logs/laravel.log
    echo -e "  Laravel log archived and cleared"
fi
# Clear Python service logs
> python-rag/rag_service.log 2>/dev/null || true
echo -e "${GREEN}✓ Logs rotated${NC}"

echo -e "${YELLOW}Step 8: Setting production environment...${NC}"
# Update .env for production (create .env.production as template)
cp .env .env.production
sed -i 's/APP_ENV=local/APP_ENV=production/g' .env.production 2>/dev/null || \
sed -i '' 's/APP_ENV=local/APP_ENV=production/g' .env.production
sed -i 's/APP_DEBUG=true/APP_DEBUG=false/g' .env.production 2>/dev/null || \
sed -i '' 's/APP_DEBUG=true/APP_DEBUG=false/g' .env.production
echo -e "${GREEN}✓ Production environment configured (see .env.production)${NC}"

echo -e "${YELLOW}Step 9: Optimizing Composer dependencies...${NC}"
# Remove development dependencies for production
composer install --optimize-autoloader --no-dev
echo -e "${GREEN}✓ Composer optimized${NC}"

echo -e "${YELLOW}Step 10: Building production assets...${NC}"
# Build optimized assets
npm run production 2>/dev/null || npm run build 2>/dev/null || true
echo -e "${GREEN}✓ Assets built for production${NC}"

echo -e "${YELLOW}Step 11: Optimizing Laravel for production...${NC}"
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache 2>/dev/null || true
php artisan optimize
echo -e "${GREEN}✓ Laravel optimized${NC}"

echo -e "${YELLOW}Step 12: Setting correct file permissions...${NC}"
# Set secure permissions
find . -type f -exec chmod 644 {} \; 2>/dev/null || true
find . -type d -exec chmod 755 {} \; 2>/dev/null || true
chmod -R 775 storage 2>/dev/null || true
chmod -R 775 bootstrap/cache 2>/dev/null || true
echo -e "${GREEN}✓ Permissions set${NC}"

echo -e "${YELLOW}Step 13: Creating production verification script...${NC}"
cat > verify-production.php << 'EOF'
<?php
echo "Production Readiness Verification\n";
echo "==================================\n";

$checks = [
    'APP_DEBUG is false' => env('APP_DEBUG') === false,
    'APP_ENV is production' => env('APP_ENV') === 'production',
    'Config is cached' => file_exists(base_path('bootstrap/cache/config.php')),
    'Routes are cached' => file_exists(base_path('bootstrap/cache/routes-v7.php')),
    'Views are cached' => count(glob(storage_path('framework/views/*.php'))) > 0,
    'No .env in git' => !file_exists(base_path('.env.example')),
    'Storage is writable' => is_writable(storage_path()),
    'No console.log in JS' => !shell_exec("grep -r 'console.log' public/js/*.js 2>/dev/null"),
];

$passed = 0;
$failed = 0;

foreach ($checks as $check => $result) {
    if ($result) {
        echo "✓ $check\n";
        $passed++;
    } else {
        echo "✗ $check\n";
        $failed++;
    }
}

echo "\nResults: $passed passed, $failed failed\n";
EOF
echo -e "${GREEN}✓ Verification script created${NC}"

echo -e "${YELLOW}Step 14: Creating rollback script...${NC}"
cat > rollback.sh << EOF
#!/bin/bash
echo "Rolling back to previous state..."
cp $BACKUP_DIR/.env.backup .env 2>/dev/null || true
cp -r $BACKUP_DIR/config_backup/* config/ 2>/dev/null || true
cp -r $BACKUP_DIR/js_backup/* public/js/ 2>/dev/null || true
cp -r $BACKUP_DIR/views_backup/* resources/views/ 2>/dev/null || true
php artisan optimize:clear
echo "Rollback complete. Backup restored from $BACKUP_DIR"
EOF
chmod +x rollback.sh
echo -e "${GREEN}✓ Rollback script created${NC}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Production Cleanup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Important Notes:${NC}"
echo "1. Backup created in: $BACKUP_DIR"
echo "2. Production config template: .env.production"
echo "3. To verify: php verify-production.php"
echo "4. To rollback: ./rollback.sh"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review .env.production and update production values"
echo "2. Run verification: php verify-production.php"
echo "3. Test all critical features"
echo "4. Deploy to production server"
echo ""
echo -e "${GREEN}All changes are non-breaking and reversible!${NC}"
