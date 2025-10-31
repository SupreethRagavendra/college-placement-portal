import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
    ],
    build: {
        // Production optimizations - using esbuild (faster, no extra dependency)
        minify: 'esbuild',
        rollupOptions: {
            output: {
                manualChunks: {
                    // Split vendor code for better caching
                    'vendor': ['alpinejs'],
                },
            },
        },
        // Enable source maps for debugging (can disable in production)
        sourcemap: false,
        // Chunk size warnings
        chunkSizeWarningLimit: 1000,
        // Enable CSS code splitting
        cssCodeSplit: true,
        // Asset inlining threshold (bytes)
        assetsInlineLimit: 4096,
    },
    server: {
        hmr: {
            host: 'localhost',
        },
    },
    optimizeDeps: {
        include: ['alpinejs'],
    },
});
