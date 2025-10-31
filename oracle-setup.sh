#!/bin/bash
#################################################
# Oracle Cloud - Automated Setup Script
# College Placement Portal Deployment
#################################################

set -e  # Exit on error

echo "================================="
echo "🚀 Oracle Cloud Setup Script"
echo "College Placement Portal"
echo "================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please run as ubuntu user, not root"
    exit 1
fi

print_info "Starting automated setup..."
echo ""

#################################################
# Part 1: System Update & Firewall
#################################################
print_info "Part 1: Updating system and configuring firewall..."

sudo apt update
sudo apt upgrade -y
print_success "System updated"

# Configure firewall
sudo apt install -y iptables-persistent
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8001 -j ACCEPT
sudo netfilter-persistent save
print_success "Firewall configured"

echo ""

#################################################
# Part 2: Install Software
#################################################
print_info "Part 2: Installing required software..."

# Add PHP repository
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update

# Install PHP 8.2 and extensions
print_info "Installing PHP 8.2..."
sudo apt install -y php8.2 php8.2-fpm php8.2-cli php8.2-pgsql php8.2-mbstring \
    php8.2-xml php8.2-curl php8.2-zip php8.2-gd php8.2-bcmath php8.2-opcache
print_success "PHP 8.2 installed"

# Install Nginx
print_info "Installing Nginx..."
sudo apt install -y nginx
print_success "Nginx installed"

# Install Node.js 20.x
print_info "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
print_success "Node.js $(node -v) installed"

# Install Composer
print_info "Installing Composer..."
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
sudo chmod +x /usr/local/bin/composer
print_success "Composer installed"

# Install Python and pip
print_info "Installing Python..."
sudo apt install -y python3 python3-pip python3-venv
print_success "Python $(python3 --version) installed"

# Install other tools
sudo apt install -y git supervisor postgresql-client
print_success "Additional tools installed"

echo ""

#################################################
# Part 3: Clone and Setup Laravel
#################################################
print_info "Part 3: Cloning repository and setting up Laravel..."

# Prompt for GitHub repository
echo ""
print_info "Enter your GitHub repository URL:"
print_info "Example: https://github.com/username/college-placement-portal.git"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    print_error "Repository URL is required!"
    exit 1
fi

# Clone repository
sudo mkdir -p /var/www
cd /var/www

if [ -d "/var/www/college-placement-portal" ]; then
    print_info "Directory exists, removing..."
    sudo rm -rf /var/www/college-placement-portal
fi

print_info "Cloning repository..."
sudo git clone "$REPO_URL" college-placement-portal
cd college-placement-portal
sudo chown -R ubuntu:ubuntu /var/www/college-placement-portal
print_success "Repository cloned"

# Install PHP dependencies
print_info "Installing PHP dependencies (this may take 5-10 minutes)..."
composer install --no-dev --optimize-autoloader --no-interaction
print_success "PHP dependencies installed"

# Install Node dependencies
print_info "Installing Node dependencies (this may take 5-10 minutes)..."
npm install
print_success "Node dependencies installed"

# Build frontend assets
print_info "Building frontend assets..."
npm run build
print_success "Frontend assets built"

# Create directories
mkdir -p storage/framework/cache/data
mkdir -p storage/framework/sessions
mkdir -p storage/framework/views
mkdir -p storage/logs
mkdir -p bootstrap/cache
print_success "Directories created"

echo ""

#################################################
# Part 4: Configure Environment
#################################################
print_info "Part 4: Configuring environment..."

# Copy .env file
if [ ! -f .env ]; then
    cp .env.example .env
    print_success ".env file created"
else
    print_info ".env file already exists, skipping..."
fi

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
print_success "Detected public IP: $PUBLIC_IP"

# Prompt for database credentials
echo ""
print_info "Database Configuration:"
read -p "DB Host (press Enter for Supabase default): " DB_HOST
DB_HOST=${DB_HOST:-db.wkqbukidxmzbgwauncrl.supabase.co}

read -p "DB Port (press Enter for 6543): " DB_PORT
DB_PORT=${DB_PORT:-6543}

read -p "DB Database (press Enter for postgres): " DB_DATABASE
DB_DATABASE=${DB_DATABASE:-postgres}

read -p "DB Username: " DB_USERNAME
read -sp "DB Password: " DB_PASSWORD
echo ""

# Update .env file
sed -i "s|APP_URL=.*|APP_URL=http://$PUBLIC_IP|g" .env
sed -i "s|APP_ENV=.*|APP_ENV=production|g" .env
sed -i "s|APP_DEBUG=.*|APP_DEBUG=false|g" .env
sed -i "s|DB_HOST=.*|DB_HOST=$DB_HOST|g" .env
sed -i "s|DB_PORT=.*|DB_PORT=$DB_PORT|g" .env
sed -i "s|DB_DATABASE=.*|DB_DATABASE=$DB_DATABASE|g" .env
sed -i "s|DB_USERNAME=.*|DB_USERNAME=$DB_USERNAME|g" .env
sed -i "s|DB_PASSWORD=.*|DB_PASSWORD=\"$DB_PASSWORD\"|g" .env
sed -i "s|DB_SSLMODE=.*|DB_SSLMODE=require|g" .env

print_success "Environment configured"

# Generate app key
print_info "Generating application key..."
php artisan key:generate --force
print_success "Application key generated"

# Set permissions
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
print_success "Permissions set"

# Run migrations
print_info "Running database migrations..."
if php artisan migrate --force; then
    print_success "Migrations completed"
else
    print_error "Migrations failed - please check database credentials"
fi

# Seed admin user
print_info "Seeding admin user..."
php artisan db:seed --class=AdminSeeder --force || print_info "Admin user may already exist"

# Cache configuration
print_info "Caching configuration..."
php artisan config:cache
php artisan route:cache
php artisan view:cache
print_success "Configuration cached"

echo ""

#################################################
# Part 5: Configure Nginx
#################################################
print_info "Part 5: Configuring Nginx..."

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/college-placement-portal > /dev/null <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name $PUBLIC_IP;
    
    root /var/www/college-placement-portal/public;
    index index.php index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/college-portal-access.log;
    error_log /var/log/nginx/college-portal-error.log;

    # Main location
    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }

    # PHP-FPM
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME \$realpath_root\$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_read_timeout 300;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
    }

    # Static assets caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # RAG Service Proxy
    location /api/rag/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/college-placement-portal /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
if sudo nginx -t; then
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    print_success "Nginx configured and started"
else
    print_error "Nginx configuration failed"
fi

# Restart PHP-FPM
sudo systemctl restart php8.2-fpm
sudo systemctl enable php8.2-fpm
print_success "PHP-FPM started"

echo ""

#################################################
# Part 6: Setup Python RAG Service
#################################################
print_info "Part 6: Setting up Python RAG service..."

cd /var/www/college-placement-portal/python-rag

# Create virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn chromadb openai httpx sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings
print_success "Python dependencies installed"

# Create .env for RAG service
cat > .env <<EOF
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_NAME=$DB_DATABASE
DB_USER=$DB_USERNAME
DB_PASSWORD=$DB_PASSWORD
OPENROUTER_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=production
EOF
print_success "RAG service environment configured"

# Create Supervisor configuration
sudo tee /etc/supervisor/conf.d/rag-service.conf > /dev/null <<EOF
[program:rag-service]
process_name=%(program_name)s
command=/var/www/college-placement-portal/python-rag/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8001
directory=/var/www/college-placement-portal/python-rag
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/rag-service.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
environment=PATH="/var/www/college-placement-portal/python-rag/venv/bin"
EOF

# Start RAG service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start rag-service
print_success "RAG service started"

echo ""

#################################################
# Part 7: Create Deployment Script
#################################################
print_info "Part 7: Creating deployment script..."

cd /var/www/college-placement-portal

cat > deploy.sh <<'EOF'
#!/bin/bash
echo "🚀 Deploying updates..."

cd /var/www/college-placement-portal

# Pull changes
git pull origin main

# Update dependencies
composer install --no-dev --optimize-autoloader
npm install
npm run build

# Run migrations
php artisan migrate --force

# Clear cache
php artisan config:clear
php artisan cache:clear
php artisan view:clear

# Rebuild cache
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Set permissions
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache

# Restart services
sudo systemctl restart php8.2-fpm
sudo supervisorctl restart rag-service

echo "✅ Deployment complete!"
EOF

chmod +x deploy.sh
print_success "Deployment script created"

echo ""

#################################################
# Part 8: Final Steps
#################################################
print_info "Part 8: Final configuration..."

# Enable PHP OPcache
sudo tee -a /etc/php/8.2/fpm/php.ini > /dev/null <<EOF

; OPcache settings
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=10000
opcache.revalidate_freq=2
opcache.fast_shutdown=1
EOF

sudo systemctl restart php8.2-fpm
print_success "PHP OPcache enabled"

# Create health check script
cat > /var/www/college-placement-portal/check-services.sh <<'EOF'
#!/bin/bash
echo "🔍 Service Status Check"
echo "======================="
echo ""
echo "Nginx:"
sudo systemctl status nginx | grep Active
echo ""
echo "PHP-FPM:"
sudo systemctl status php8.2-fpm | grep Active
echo ""
echo "RAG Service:"
sudo supervisorctl status rag-service
echo ""
echo "Disk Usage:"
df -h | grep -E 'Filesystem|/$'
echo ""
echo "Memory Usage:"
free -h
EOF

chmod +x /var/www/college-placement-portal/check-services.sh
print_success "Health check script created"

echo ""
echo "================================="
print_success "Setup Complete! 🎉"
echo "================================="
echo ""
echo "📊 Your Application Details:"
echo "----------------------------"
echo "URL: http://$PUBLIC_IP"
echo "Admin Login: admin@portal.com"
echo "Admin Password: Admin@123"
echo "RAG Service: http://$PUBLIC_IP:8001/health"
echo ""
echo "🔧 Useful Commands:"
echo "-------------------"
echo "Check services: ./check-services.sh"
echo "Deploy updates: ./deploy.sh"
echo "View logs: sudo tail -f /var/log/nginx/college-portal-error.log"
echo "Restart all: sudo systemctl restart nginx php8.2-fpm && sudo supervisorctl restart rag-service"
echo ""
echo "📚 Documentation:"
echo "-----------------"
echo "Full guide: /var/www/college-placement-portal/ORACLE_CLOUD_DEPLOYMENT_GUIDE.md"
echo ""
print_success "Everything is ready!"
echo ""

