<!-- c6d82c60-fd9f-43be-a185-c2d93c3e79ec 5d96d465-7a95-4601-a850-38821839c626 -->
# Fix Database Timeout on Slow Internet

## Problem

The application uses a remote PostgreSQL database (Supabase) for cache storage. When internet is slow, cache queries timeout causing `SQLSTATE[08006] [7] timeout expired` errors.

## Solution Overview

1. Switch cache driver from `database` to `file` storage (local disk)
2. Increase PostgreSQL connection timeouts for better resilience
3. Add connection retry logic
4. Keep session storage local (already using `file` driver)

## Implementation Steps

### 1. Update Cache Configuration (`config/cache.php`)

- Change default cache store from `database` to `file`
- File cache stores data locally in `storage/framework/cache/data`
- No internet required for cache operations

### 2. Update Database Configuration (`config/database.php`)

- Increase `PDO::ATTR_TIMEOUT` from 30 to 90 seconds for main connection
- Add `connect_timeout` option (60 seconds)
- Add connection retry settings
- Keep longer timeout (60s) for `pgsql_cache` connection

### 3. Add Environment Variables Documentation

- Document recommended local development settings
- Create `.env.example` updates for cache configuration

## Key Files to Modify

- `config/cache.php` - Switch default to 'file'
- `config/database.php` - Increase timeouts and add retry logic

## Benefits

- **Fast local caching**: No internet needed for cache operations
- **Resilient database queries**: Longer timeouts prevent premature failures
- **Works on slow internet**: Application remains functional even with poor connectivity
- **Production-ready**: File cache works both locally and on production servers

### To-dos

- [ ] Update config/cache.php to use 'file' driver as default instead of database
- [ ] Increase PostgreSQL connection timeouts in config/database.php to 90s with 60s connect timeout
- [ ] Add connection retry and resilience settings to database configuration
- [ ] Clear existing cache to ensure clean state after configuration changes