#!/usr/bin/env bash
# Final deployment script for Render

echo "🚀 Preparing deployment to Render..."

# Check if we're in the right directory
if [ ! -f "composer.json" ]; then
    echo "❌ Error: Not in Laravel project directory"
    exit 1
fi

echo "✅ Laravel project detected"

# Add all changes
echo "📦 Adding all changes to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Fix: Resolve 500 error - Add TrustProxies, health checks, and improve Render compatibility"

# Push to main branch
echo "🚀 Pushing to main branch..."
git push origin main

echo ""
echo "================================"
echo "🎯 DEPLOYMENT COMPLETE!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Go to Render Dashboard: https://dashboard.render.com"
echo "2. Find your 'college-placement-portal' service"
echo "3. Click 'Environment' tab"
echo "4. Add these REQUIRED environment variables:"
echo ""
echo "   APP_KEY=base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4="
echo "   DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co"
echo "   DB_DATABASE=postgres"
echo "   DB_USERNAME=postgres"
echo "   DB_PASSWORD=Supreeeth24#"
echo ""
echo "5. Click 'Save Changes' and wait for redeploy"
echo ""
echo "🔍 Test endpoints after deployment:"
echo "   • Health check: https://college-placement-portals.onrender.com/health.php"
echo "   • PHP test: https://college-placement-portals.onrender.com/test.php"
echo "   • DB test: https://college-placement-portals.onrender.com/test-db"
echo "   • Main site: https://college-placement-portals.onrender.com"
echo ""
echo "⏱️  First load may take 30-60 seconds (free tier cold start)"
echo ""
