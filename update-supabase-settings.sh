#!/bin/bash

# Update Supabase settings using API
echo "Updating Supabase settings..."

# Get your project reference
PROJECT_REF="wkqbukidxmzbgwauncrl"
SERVICE_ROLE_KEY="your_service_role_key_here"

# Update site URL and redirect URLs
curl -X PATCH "https://api.supabase.com/v1/projects/$PROJECT_REF/config/auth" \
  -H "Authorization: Bearer $SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "SITE_URL": "http://localhost:8000",
    "REDIRECT_URLS": [
      "http://localhost:8000/auth/callback",
      "http://localhost:8000/password/reset"
    ]
  }'

echo "Settings updated!"
