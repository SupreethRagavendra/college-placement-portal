#!/bin/bash

# Supabase Edge Function Deployment Script
# This script deploys the email notification Edge Function to Supabase

echo "🚀 Deploying Supabase Edge Function for Email Notifications"
echo "============================================================"

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI is not installed. Installing..."
    npm install -g supabase
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Supabase CLI. Please install manually:"
        echo "   npm install -g supabase"
        exit 1
    fi
fi

# Check if user is logged in
echo "🔐 Checking Supabase authentication..."
if ! supabase status &> /dev/null; then
    echo "🔑 Please login to Supabase:"
    supabase login
    if [ $? -ne 0 ]; then
        echo "❌ Login failed. Please try again."
        exit 1
    fi
fi

# Check if project is linked
echo "🔗 Checking project link..."
if [ ! -f ".supabase/config.toml" ]; then
    echo "📝 Project not linked. Please provide your project reference ID:"
    read -p "Project Reference ID: " project_ref
    supabase link --project-ref $project_ref
    if [ $? -ne 0 ]; then
        echo "❌ Failed to link project. Please check your project reference ID."
        exit 1
    fi
fi

# Deploy the Edge Function
echo "📦 Deploying send-status-email Edge Function..."
supabase functions deploy send-status-email
if [ $? -ne 0 ]; then
    echo "❌ Function deployment failed. Please check your function code and try again."
    exit 1
fi

echo "✅ Edge Function deployed successfully!"
echo ""

# Prompt for environment variables
echo "🔧 Setting up environment variables..."
echo "============================================="

# SendGrid API Key
echo "📧 SendGrid Configuration:"
echo "1. Go to https://sendgrid.com/ and create an account"
echo "2. Navigate to Settings > API Keys"
echo "3. Create a new API key with 'Mail Send' permissions"
echo ""
read -p "Enter your SendGrid API Key: " sendgrid_key
if [ ! -z "$sendgrid_key" ]; then
    supabase secrets set SENDGRID_API_KEY="$sendgrid_key"
    echo "✅ SendGrid API key set"
else
    echo "⚠️  Skipping SendGrid API key (you can set it later)"
fi

# From Email
echo ""
read -p "Enter your FROM email address (must be verified in SendGrid): " from_email
if [ ! -z "$from_email" ]; then
    supabase secrets set FROM_EMAIL="$from_email"
    echo "✅ From email set"
else
    echo "⚠️  Skipping from email (you can set it later)"
fi

# From Name
echo ""
read -p "Enter your FROM name (e.g., 'College Placement Portal'): " from_name
if [ ! -z "$from_name" ]; then
    supabase secrets set FROM_NAME="$from_name"
    echo "✅ From name set"
else
    echo "⚠️  Skipping from name (you can set it later)"
fi

# Portal URL
echo ""
read -p "Enter your portal URL (e.g., https://yourportal.com): " portal_url
if [ ! -z "$portal_url" ]; then
    supabase secrets set PORTAL_URL="$portal_url"
    echo "✅ Portal URL set"
else
    echo "⚠️  Skipping portal URL (you can set it later)"
fi

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "📋 Next Steps:"
echo "1. Verify your sender email in SendGrid"
echo "2. Test the function using the test script or Laravel"
echo "3. Monitor function logs: supabase functions logs send-status-email"
echo ""

# Offer to run a test
echo "🧪 Would you like to run a test email? (y/n)"
read -p "" test_choice
if [[ $test_choice == "y" || $test_choice == "Y" ]]; then
    echo ""
    echo "📧 Test Email Configuration:"
    read -p "Test recipient email: " test_email
    read -p "Test recipient name: " test_name
    
    echo "Sending test approval email..."
    
    # Get project URL for API call
    project_url=$(grep 'project_url' .supabase/config.toml | cut -d'"' -f2)
    anon_key=$(grep 'anon_key' .supabase/config.toml | cut -d'"' -f2)
    
    if [ ! -z "$project_url" ] && [ ! -z "$anon_key" ]; then
        curl -X POST "${project_url}/functions/v1/send-status-email" \
             -H "Authorization: Bearer ${anon_key}" \
             -H "Content-Type: application/json" \
             -d "{
                 \"student_email\": \"$test_email\",
                 \"student_name\": \"$test_name\",
                 \"status\": \"approved\"
             }"
        echo ""
        echo "✅ Test email sent! Check your inbox and spam folder."
    else
        echo "❌ Could not retrieve project configuration for test."
    fi
fi

echo ""
echo "📚 For more information, see: EMAIL_NOTIFICATION_SETUP.md"
echo "🐛 If you encounter issues, check function logs: supabase functions logs send-status-email"