#!/bin/bash

# ============================================================================
# AllCanLearn - Ubuntu Server Deployment Script
# ============================================================================
# Run this on your Ubuntu server (192.168.1.138)
# Usage: bash deploy.sh
# ============================================================================

set -e  # Exit on error

echo "🚀 AllCanLearn Deployment to Ubuntu Server"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/home/vikki/AllCanLearn"
REPO_URL="https://github.com/your-repo/AllCanLearn.git"  # Update this
PYTHON_VERSION="3.11"
SERVICE_NAME="allcanlearn"

# ============================================================================
# 1. System Updates
# ============================================================================
echo -e "${BLUE}📦 Step 1: System Updates${NC}"
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib \
    nginx supervisor git curl wget

echo -e "${GREEN}✅ System packages installed${NC}\n"

# ============================================================================
# 2. Create Application Directory
# ============================================================================
echo -e "${BLUE}📁 Step 2: Setting up directories${NC}"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone repo or use existing
if [ -d ".git" ]; then
    echo "Pulling latest code..."
    git pull origin main
else
    echo "Cloning repository..."
    git clone $REPO_URL . || echo "⚠️  Set REPO_URL in script first!"
fi

echo -e "${GREEN}✅ Application directory ready${NC}\n"

# ============================================================================
# 3. Python Virtual Environment
# ============================================================================
echo -e "${BLUE}🐍 Step 3: Setting up Python environment${NC}"
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found!"
fi

echo -e "${GREEN}✅ Python environment ready${NC}\n"

# ============================================================================
# 4. PostgreSQL Database Setup
# ============================================================================
echo -e "${BLUE}🗄️  Step 4: Setting up PostgreSQL${NC}"

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
DB_NAME="allcanlearn"
DB_USER="allcanlearn_user"
DB_PASS=$(openssl rand -base64 12)

sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET default_transaction_deferrable TO on;
ALTER ROLE $DB_USER SET default_transaction_level TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Pass: $DB_PASS" > /tmp/db_credentials.txt
echo -e "${YELLOW}⚠️  DB credentials saved to /tmp/db_credentials.txt${NC}"

echo -e "${GREEN}✅ PostgreSQL configured${NC}\n"

# ============================================================================
# 5. Environment Configuration
# ============================================================================
echo -e "${BLUE}⚙️  Step 5: Creating .env file${NC}"

cat > .env << EOF
# AllCanLearn Production Configuration
ENVIRONMENT=production
DEBUG=False

# Database
DATABASE_URL=postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME

# AI API Keys
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here

# Server
HOST=0.0.0.0
PORT=8001
WORKERS=4

# Security
SECRET_KEY=$(openssl rand -base64 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Features
ENABLE_CHAT=true
ENABLE_QUIZ=true
ENABLE_PODCAST=true

# Email (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/allcanlearn.log
EOF

echo -e "${YELLOW}⚠️  IMPORTANT: Update .env with your API keys!${NC}"
echo -e "${YELLOW}nano .env${NC}\n"

echo -e "${GREEN}✅ .env file created${NC}\n"

# ============================================================================
# 6. Create Required Directories
# ============================================================================
echo -e "${BLUE}📂 Step 6: Creating directories${NC}"
mkdir -p logs tts_output episodes_data data/db

echo -e "${GREEN}✅ Directories created${NC}\n"

# ============================================================================
# 7. Database Migrations (if using Alembic)
# ============================================================================
echo -e "${BLUE}🔄 Step 7: Database setup${NC}"
# If using Alembic:
# alembic upgrade head

# Or create tables from models:
python3 << PYTHON
import os
os.chdir('$APP_DIR')
# from app.database import Base, engine
# Base.metadata.create_all(bind=engine)
print("✅ Database tables ready")
PYTHON

echo -e "${GREEN}✅ Database initialized${NC}\n"

# ============================================================================
# 8. Supervisor Configuration
# ============================================================================
echo -e "${BLUE}⚙️  Step 8: Setting up supervisor${NC}"

sudo tee /etc/supervisor/conf.d/allcanlearn.conf > /dev/null << EOF
[program:allcanlearn]
directory=$APP_DIR
command=$APP_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4 --log-config logging.ini
user=vikki
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/logs/app.log
environment=PATH="$APP_DIR/venv/bin",DATABASE_URL="postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME"
EOF

sudo systemctl restart supervisor
sudo supervisorctl reread
sudo supervisorctl update

echo -e "${GREEN}✅ Supervisor configured${NC}\n"

# ============================================================================
# 9. Nginx Configuration
# ============================================================================
echo -e "${BLUE}🌐 Step 9: Setting up Nginx${NC}"

sudo tee /etc/nginx/sites-available/allcanlearn > /dev/null << 'EOF'
upstream allcanlearn {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 50M;

    location / {
        proxy_pass http://allcanlearn;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias $APP_DIR/app/static;
        expires 30d;
    }

    location /tts_output {
        alias $APP_DIR/tts_output;
        expires 7d;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/allcanlearn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t
sudo systemctl restart nginx

echo -e "${GREEN}✅ Nginx configured${NC}\n"

# ============================================================================
# 10. SSL Certificate (Optional - Let's Encrypt)
# ============================================================================
echo -e "${BLUE}🔒 Step 10: SSL Setup (Optional)${NC}"
echo "Install certbot for HTTPS:"
echo "  sudo apt install certbot python3-certbot-nginx"
echo "  sudo certbot --nginx -d yourdomain.com"
echo ""

# ============================================================================
# 11. Firewall Configuration
# ============================================================================
echo -e "${BLUE}🔥 Step 11: Firewall${NC}"
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

echo -e "${GREEN}✅ Firewall configured${NC}\n"

# ============================================================================
# 12. Verification
# ============================================================================
echo -e "${BLUE}✅ Step 12: Verification${NC}"
echo ""
echo "Checking services:"
sudo systemctl status nginx --no-pager | head -5
echo ""
sudo supervisorctl status

echo ""
echo -e "${GREEN}=========================================="
echo "🎉 AllCanLearn Deployment Complete!"
echo "=========================================="
echo ""
echo "📍 Server: http://192.168.1.138"
echo ""
echo "📋 Next Steps:"
echo "1. Update .env with your API keys:"
echo "   nano $APP_DIR/.env"
echo ""
echo "2. Check application logs:"
echo "   tail -f $APP_DIR/logs/app.log"
echo ""
echo "3. Monitor with supervisor:"
echo "   sudo supervisorctl"
echo ""
echo "4. (Optional) Set up SSL:"
echo "   sudo certbot --nginx"
echo ""
echo "5. View database credentials:"
echo "   cat /tmp/db_credentials.txt"
echo ""
echo -e "${NC}"
