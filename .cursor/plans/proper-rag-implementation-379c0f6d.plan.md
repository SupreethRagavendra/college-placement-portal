<!-- 379c0f6d-ffd3-463d-8c3e-5a96f913ca10 261c54ab-0832-461e-89f4-63703b4aeae0 -->
# Website Performance Optimization Plan

## Overview

Optimize loading speed and performance across the entire website without breaking any existing functionality.

## Optimizations to Implement

### 1. Asset Optimization

**Files:** All Blade templates (landing.blade.php, layouts/app.blade.php, layouts/student.blade.php, layouts/admin.blade.php)

- Add `defer` attribute to non-critical JavaScript (Bootstrap, Font Awesome)
- Move JavaScript to bottom before `</body>`
- Add `preload` for critical resources (fonts, CSS)
- Add `async` to Font Awesome and other icon libraries
- Optimize external font loading with `font-display: swap`

### 2. Image Optimization

**Files:** landing.blade.php, layouts/app.blade.php, layouts/student.blade.php

- Add `loading="lazy"` to all images below the fold
- Add proper `width` and `height` attributes to prevent layout shift
- Compress logo image (logo1-removebg-preview.png)
- Use WebP format with fallback for hero section background

### 3. CSS Optimization

**Files:** All layout files

- Minify inline CSS in `<style>` tags
- Move non-critical CSS to bottom or use `media="print" onload="this.media='all'"`
- Extract common styles to external cached CSS file
- Remove duplicate CSS rules across layouts

### 4. Caching Implementation

**Files:** config/cache.php, routes/web.php, app/Http/Middleware/*, config/view.php

- Enable view caching: `php artisan view:cache`
- Enable route caching: `php artisan route:cache`
- Enable config caching: `php artisan config:cache`
- Add browser cache headers for static assets
- Implement response caching for public pages

### 5. Database Query Optimization

**Files:** All Controller files

- Add eager loading to prevent N+1 queries
- Cache frequently accessed data (assessments list, student context)
- Add database indexes for common queries
- Optimize existing cache TTL values

### 6. JavaScript Optimization

**Files:** public/js/chatbot.js

- Minify chatbot.js
- Remove console.log statements
- Defer chatbot initialization until user interaction
- Use passive event listeners where possible

### 7. HTTP/2 Server Push (if available)

**Files:** public/.htaccess or nginx config

- Add headers for preloading critical CSS and JS
- Enable gzip/brotli compression
- Set proper cache-control headers

### 8. Reduce External Dependencies

**Files:** All Blade templates

- Use CDN with integrity checks and crossorigin
- Add fallback for CDN failures
- Consider self-hosting critical resources

### 9. Laravel Optimizations

**Files:** config/app.php, composer.json

- Disable debug mode in production
- Use OPcache for PHP
- Enable Laravel Octane (optional, requires setup)
- Optimize autoloader: `composer dump-autoload --optimize`

### 10. Lazy Load Components

**Files:** layouts/student.blade.php (chatbot)

- Load chatbot component only when chat button is clicked
- Defer analytics scripts
- Load non-critical components asynchronously

## Implementation Order

1. Asset optimization (immediate impact)
2. Image optimization (immediate impact)
3. Caching implementation (high impact)
4. CSS optimization (medium impact)
5. Database query optimization (high impact for dynamic pages)
6. JavaScript optimization (medium impact)
7. Laravel optimizations (production only)
8. HTTP headers and compression (requires server access)

## Files to Modify

- resources/views/landing.blade.php
- resources/views/layouts/app.blade.php
- resources/views/layouts/student.blade.php
- resources/views/layouts/admin.blade.php
- public/js/chatbot.js
- config/cache.php
- All controller files (for query optimization)
- public/.htaccess (for headers)

## Testing Required

- Test all pages load correctly
- Verify chatbot functionality
- Check student dashboard performance
- Test admin panel operations
- Verify image loading
- Test on slow 3G connection

## Expected Results

- 40-60% reduction in initial page load time
- Improved Time to First Byte (TTFB)
- Better Core Web Vitals scores (LCP, FID, CLS)
- Reduced server load
- Better mobile performance

### To-dos

- [ ] Set up ChromaDB vector database and install dependencies
- [ ] Create vector_store.py with embedding and search functionality
- [ ] Create knowledge base directory with FAQs, guidelines, and study tips
- [ ] Create init_vector_db.py script and populate vector database
- [ ] Update context_handler.py and main.py to use vector store
- [ ] Create chatbot_conversations migration and run it
- [ ] Update OpenRouterChatbotController with conversation memory
- [ ] Update Python RAG to accept and use conversation history
- [ ] Implement student context caching in Laravel controller
- [ ] Create response_cache.py and integrate with main.py
- [ ] Create chatbot_analytics migration and run it
- [ ] Add analytics logging to Laravel controller
- [ ] Create and run test_rag_system.py to verify functionality
- [ ] Run deployment checklist and verify system is working