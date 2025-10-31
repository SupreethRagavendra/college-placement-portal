#!/bin/bash
# Script to help set up Render environment variables

echo "================================================"
echo "🔧 Render Environment Variables Setup Helper"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}This script will help you set up environment variables for Render.${NC}"
echo ""

# Generate APP_KEY if needed
echo "================================================"
echo "1️⃣  Generating Laravel APP_KEY"
echo "================================================"
if [ -f "artisan" ]; then
    APP_KEY=$(php artisan key:generate --show)
    echo -e "${GREEN}✅ Generated APP_KEY:${NC}"
    echo "$APP_KEY"
else
    echo -e "${RED}❌ artisan file not found. Using provided key.${NC}"
    APP_KEY="base64:Tru9xzXURTw16wL/3WUX/Ok5WYYcuDCvPxgdXWq+g/4="
    echo "$APP_KEY"
fi
echo ""

# Display all required environment variables
echo "================================================"
echo "2️⃣  Required Environment Variables"
echo "================================================"
echo ""

echo -e "${YELLOW}📋 Copy these to Render Dashboard → Environment tab:${NC}"
echo ""

echo "=== LARAVEL SERVICE (college-placement-portal) ==="
echo ""
echo "APP_KEY=$APP_KEY"
echo "DB_PASSWORD=Supreeeth24#"
echo "GROQ_API_KEY=your_groq_api_key_here"
echo ""

echo "=== RAG SERVICE (rag-service) ==="
echo ""
echo "DB_PASSWORD=Supreeeth24#"
echo "OPENROUTER_API_KEY=your_openrouter_api_key_here"
echo ""

echo "================================================"
echo "3️⃣  Render Dashboard Settings"
echo "================================================"
echo ""

echo "Laravel Service Settings:"
echo "  - Runtime: Docker"
echo "  - Region: Oregon (US West)"
echo "  - Health Check Path: /healthz"
echo "  - Auto-Deploy: Yes"
echo ""

echo "RAG Service Settings:"
echo "  - Runtime: Docker"
echo "  - Dockerfile Path: ./python-rag/Dockerfile"
echo "  - Docker Context: ./python-rag"
echo "  - Health Check Path: /health"
echo "  - Auto-Deploy: Yes"
echo ""

echo "================================================"
echo "4️⃣  Deployment Steps"
echo "================================================"
echo ""

echo "1. Go to: https://dashboard.render.com"
echo "2. Select your service"
echo "3. Click 'Environment' tab"
echo "4. Add the variables shown above"
echo "5. Click 'Save Changes'"
echo "6. Service will auto-redeploy"
echo ""

echo "================================================"
echo "5️⃣  Testing After Deployment"
echo "================================================"
echo ""

echo "Test these URLs:"
echo "  • Health: https://college-placement-portals.onrender.com/healthz"
echo "  • DB Test: https://college-placement-portals.onrender.com/test-db"
echo "  • Main: https://college-placement-portals.onrender.com/"
echo "  • RAG: https://rag-service.onrender.com/health"
echo ""

echo -e "${GREEN}✅ Setup information generated!${NC}"
echo ""
echo "📝 Save this output for reference."
echo ""
