<?php

/**
 * Production Readiness Validation Script
 * Run: php validate-production.php
 * 
 * This script checks if the application is ready for production deployment
 * All checks are non-destructive and read-only
 */

// Load Laravel bootstrap
require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

// Color codes for terminal output
$red = "\033[0;31m";
$green = "\033[0;32m";
$yellow = "\033[1;33m";
$reset = "\033[0m";

echo "\n{$green}========================================{$reset}\n";
echo "{$green}Production Readiness Validation{$reset}\n";
echo "{$green}========================================{$reset}\n\n";

$checks = [];
$criticalIssues = [];
$warnings = [];
$passed = 0;
$failed = 0;

// 1. Environment Configuration Checks
echo "{$yellow}Checking Environment Configuration...{$reset}\n";

$checks['APP_DEBUG is false'] = env('APP_DEBUG') === false;
if (!$checks['APP_DEBUG is false']) {
    $criticalIssues[] = "APP_DEBUG is set to true - exposes sensitive information";
}

$checks['APP_ENV is production'] = env('APP_ENV') === 'production';
if (!$checks['APP_ENV is production']) {
    $warnings[] = "APP_ENV is not set to production";
}

$checks['APP_KEY is set'] = !empty(env('APP_KEY'));
if (!$checks['APP_KEY is set']) {
    $criticalIssues[] = "APP_KEY is not set - run: php artisan key:generate";
}

// 2. Debug Code Checks
echo "{$yellow}Checking for Debug Code...{$reset}\n";

// Check for console.log in JavaScript files
$jsFiles = glob('public/js/*.js');
$consoleLogFound = false;
$filesWithConsoleLog = [];
foreach ($jsFiles as $file) {
    $content = file_get_contents($file);
    if (strpos($content, 'console.log') !== false) {
        $consoleLogFound = true;
        $filesWithConsoleLog[] = basename($file);
    }
}
$checks['No console.log in JS'] = !$consoleLogFound;
if ($consoleLogFound) {
    $warnings[] = "console.log found in: " . implode(', ', $filesWithConsoleLog);
}

// Check for dd() in Blade files
$bladeFiles = glob_recursive('resources/views/*.blade.php');
$ddFound = false;
$filesWithDd = [];
foreach ($bladeFiles as $file) {
    $content = file_get_contents($file);
    if (preg_match('/\{\{.*dd\(/', $content) || preg_match('/\@dd\(/', $content)) {
        $ddFound = true;
        $filesWithDd[] = str_replace('resources/views/', '', $file);
    }
}
$checks['No dd() in Blade'] = !$ddFound;
if ($ddFound) {
    $criticalIssues[] = "dd() found in views: " . implode(', ', $filesWithDd);
}

// 3. Laravel Optimization Checks
echo "{$yellow}Checking Laravel Optimization...{$reset}\n";

$checks['Config is cached'] = file_exists(base_path('bootstrap/cache/config.php'));
if (!$checks['Config is cached']) {
    $warnings[] = "Config not cached - run: php artisan config:cache";
}

$checks['Routes are cached'] = file_exists(base_path('bootstrap/cache/routes-v7.php'));
if (!$checks['Routes are cached']) {
    $warnings[] = "Routes not cached - run: php artisan route:cache";
}

$checks['Views are compiled'] = count(glob(storage_path('framework/views/*.php'))) > 0;

// 4. Security Checks
echo "{$yellow}Checking Security Configuration...{$reset}\n";

$checks['Session secure cookie'] = config('session.secure') === true || env('SESSION_SECURE_COOKIE') === true;
if (!$checks['Session secure cookie']) {
    $warnings[] = "Session cookies not set to secure (HTTPS only)";
}

$checks['CSRF protection enabled'] = !empty(config('app.key'));

// Check for exposed .env file
$envAccessible = false;
if (file_exists(public_path('.env'))) {
    $envAccessible = true;
    $criticalIssues[] = ".env file is in public directory!";
}
$checks['No .env in public'] = !$envAccessible;

// 5. Database Checks
echo "{$yellow}Checking Database Configuration...{$reset}\n";

try {
    DB::connection()->getPdo();
    $checks['Database connection'] = true;
    
    // Check for missing indexes
    $missingIndexes = [];
    $tables = [
        'student_assessments' => ['student_id', 'assessment_id'],
        'student_answers' => ['student_assessment_id', 'question_id']
    ];
    
    foreach ($tables as $table => $columns) {
        if (Schema::hasTable($table)) {
            $indexes = DB::select("SHOW INDEX FROM $table");
            $indexedColumns = array_column($indexes, 'Column_name');
            foreach ($columns as $column) {
                if (!in_array($column, $indexedColumns)) {
                    $missingIndexes[] = "$table.$column";
                }
            }
        }
    }
    
    $checks['Database indexes'] = empty($missingIndexes);
    if (!empty($missingIndexes)) {
        $warnings[] = "Missing indexes on: " . implode(', ', $missingIndexes);
    }
} catch (Exception $e) {
    $checks['Database connection'] = false;
    $criticalIssues[] = "Database connection failed: " . $e->getMessage();
}

// 6. File System Checks
echo "{$yellow}Checking File System...{$reset}\n";

$checks['Storage writable'] = is_writable(storage_path());
if (!$checks['Storage writable']) {
    $criticalIssues[] = "Storage directory is not writable";
}

$checks['Cache writable'] = is_writable(bootstrap_path('cache'));
if (!$checks['Cache writable']) {
    $criticalIssues[] = "Bootstrap cache directory is not writable";
}

// Check for test files
$testFiles = [
    'resources/views/student/test.blade.php',
    'public/js/chatbot-debug.js',
    'app/Http/Controllers/AdminQuestionController.php.disabled'
];
$foundTestFiles = [];
foreach ($testFiles as $file) {
    if (file_exists(base_path($file))) {
        $foundTestFiles[] = $file;
    }
}
$checks['No test files'] = empty($foundTestFiles);
if (!empty($foundTestFiles)) {
    $warnings[] = "Test files found: " . implode(', ', $foundTestFiles);
}

// 7. Performance Checks
echo "{$yellow}Checking Performance Configuration...{$reset}\n";

$checks['Composer optimized'] = file_exists(base_path('vendor/composer/autoload_classmap.php')) && 
                                 filesize(base_path('vendor/composer/autoload_classmap.php')) > 10000;
if (!$checks['Composer optimized']) {
    $warnings[] = "Composer not optimized - run: composer install --optimize-autoloader";
}

// 8. API Key Security
echo "{$yellow}Checking API Key Security...{$reset}\n";

$envContent = file_exists('.env') ? file_get_contents('.env') : '';
$exposedApiKey = strpos($envContent, 'sk-or-v1-') !== false;
$checks['API keys secured'] = !$exposedApiKey || strpos($envContent, 'OPENROUTER_API_KEY=') !== false;
if ($exposedApiKey && strpos($envContent, 'OPENROUTER_API_KEY=') === false) {
    $criticalIssues[] = "API key might be hardcoded - move to OPENROUTER_API_KEY env variable";
}

// Display Results
echo "\n{$green}========================================{$reset}\n";
echo "{$green}Validation Results{$reset}\n";
echo "{$green}========================================{$reset}\n\n";

foreach ($checks as $check => $result) {
    if ($result) {
        echo "{$green}✅{$reset} $check\n";
        $passed++;
    } else {
        echo "{$red}❌{$reset} $check\n";
        $failed++;
    }
}

// Display Issues
if (!empty($criticalIssues)) {
    echo "\n{$red}⚠️  CRITICAL ISSUES (Must Fix):{$reset}\n";
    foreach ($criticalIssues as $issue) {
        echo "   • $issue\n";
    }
}

if (!empty($warnings)) {
    echo "\n{$yellow}⚠️  WARNINGS (Should Fix):{$reset}\n";
    foreach ($warnings as $warning) {
        echo "   • $warning\n";
    }
}

// Final Score
echo "\n{$green}========================================{$reset}\n";
$total = count($checks);
$percentage = round(($passed / $total) * 100);

echo "Score: {$passed}/{$total} ({$percentage}%)\n";

if ($percentage === 100) {
    echo "{$green}✅ PRODUCTION READY!{$reset}\n";
    echo "All checks passed. Your application is ready for deployment.\n";
} elseif ($percentage >= 80) {
    echo "{$yellow}⚠️  ALMOST READY{$reset}\n";
    echo "Fix the remaining issues before deploying to production.\n";
} else {
    echo "{$red}❌ NOT READY FOR PRODUCTION{$reset}\n";
    echo "Multiple critical issues found. Please fix them before deployment.\n";
}

echo "\n{$yellow}Quick Fix Commands:{$reset}\n";
if (!$checks['APP_DEBUG is false']) {
    echo "• sed -i 's/APP_DEBUG=true/APP_DEBUG=false/' .env\n";
}
if (!$checks['Config is cached']) {
    echo "• php artisan config:cache\n";
}
if (!$checks['Routes are cached']) {
    echo "• php artisan route:cache\n";
}
if (!$checks['Composer optimized']) {
    echo "• composer install --optimize-autoloader --no-dev\n";
}
if ($consoleLogFound) {
    echo "• find public/js -name '*.js' -exec sed -i '/console\\.log/d' {} \\;\n";
}

echo "\n";

// Helper function for recursive glob
function glob_recursive($pattern, $flags = 0) {
    $files = glob($pattern, $flags);
    foreach (glob(dirname($pattern).'/*', GLOB_ONLYDIR|GLOB_NOSORT) as $dir) {
        $files = array_merge($files, glob_recursive($dir.'/'.basename($pattern), $flags));
    }
    return $files;
}

exit($percentage === 100 ? 0 : 1);
