<?php

require_once 'vendor/autoload.php';

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Artisan;

// Bootstrap Laravel
$app = require_once 'bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

echo "=== Database Timeout Fix Script ===\n\n";

try {
    // Test database connection
    echo "1. Testing database connection...\n";
    $connection = DB::connection();
    $connection->getPdo();
    echo "✓ Database connection successful\n\n";
    
    // Clear all caches
    echo "2. Clearing application caches...\n";
    Artisan::call('cache:clear');
    echo "✓ Application cache cleared\n";
    
    Artisan::call('config:clear');
    echo "✓ Configuration cache cleared\n";
    
    Artisan::call('route:clear');
    echo "✓ Route cache cleared\n";
    
    Artisan::call('view:clear');
    echo "✓ View cache cleared\n\n";
    
    // Test cache operations
    echo "3. Testing cache operations...\n";
    Cache::put('test_key', 'test_value', 60);
    $value = Cache::get('test_key');
    if ($value === 'test_value') {
        echo "✓ Cache operations working correctly\n";
        Cache::forget('test_key');
    } else {
        echo "✗ Cache operations failed\n";
    }
    
    echo "\n4. Testing database query...\n";
    $result = DB::select('SELECT 1 as test');
    if (!empty($result)) {
        echo "✓ Database queries working correctly\n";
    } else {
        echo "✗ Database queries failed\n";
    }
    
    echo "\n=== Fix completed successfully ===\n";
    
} catch (Exception $e) {
    echo "✗ Error: " . $e->getMessage() . "\n";
    echo "Stack trace:\n" . $e->getTraceAsString() . "\n";
}
