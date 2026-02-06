# 🚀 AllCanLearn v4 - Ubuntu Server Deployment Guide

## 📋 Prerequisites

### Ubuntu Server Requirements
- Ubuntu 20.04+ (recommended 22.04 LTS)
- Minimum 2GB RAM, 4GB recommended
- 10GB+ storage space
- Internet connection

### Required Software
- Python 3.9+
- Node.js 18+
- npm
- Git
- FFmpeg (for audio processing)

## 🔧 Step-by-Step Setup

### 1. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install System Dependencies
```bash
# Install Python and build tools
sudo apt install -y python3 python3-pip python3-venv build-essential

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install FFmpeg for audio processing
sudo apt install -y ffmpeg

# Install Git (if not installed)
sudo apt install -y git
```

### 3. Create Application Directory
```bash
# Create app directory
sudo mkdir -p /var/www/allcanlearn
sudo chown $USER:$USER /var/www/allcanlearn
cd /var/www/allcanlearn
```

### 4. Clone Your Application
```bash
# Clone from your repository (replace with your actual repo URL)
git clone <YOUR_REPOSITORY_URL> .

# OR copy files from your local machine
# scp -r /path/to/AllCanLearn-v4/* user@server:/var/www/allcanlearn/
```

### 5. Setup Python Backend
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
nano .env  # Add your GROQ_API_KEY and other secrets
```

### 6. Setup React Frontend
```bash
# Install Node.js dependencies
npm install

# Build the React app for production
npm run build

# Copy build files to public directory
cp -r build/* public/
```

### 7. Create Systemd Service for Backend
```bash
sudo nano /etc/systemd/system/allcanlearn.service
```

Add this content to the service file:
```ini
[Unit]
Description=AllCanLearn Backend Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/allcanlearn
Environment=PATH=/var/www/allcanlearn/venv/bin
ExecStart=/var/www/allcanlearn/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 8. Setup Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/allcanlearn
```

Add this Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or IP

    # Serve static files directly
    location / {
        root /var/www/allcanlearn/public;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy generate endpoint
    location /generate {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve audio files
    location /tts_output {
        alias /var/www/allcanlearn/tts_output;
        expires 3d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 9. Enable and Start Services
```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/allcanlearn /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test Nginx configuration
sudo nginx -t

# Start and enable services
sudo systemctl start allcanlearn
sudo systemctl enable allcanlearn
sudo systemctl start nginx
sudo systemctl enable nginx

# Check service status
sudo systemctl status allcanlearn
sudo systemctl status nginx
```

### 10. Setup Firewall
```bash
# Allow HTTP and HTTPS traffic
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw enable
```

### 11. Setup SSL Certificate (Optional but Recommended)
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Auto-renew certificates
sudo crontab -e
# Add this line:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📁 Directory Structure After Setup
```
/var/www/allcanlearn/
├── app/                    # Python backend
├── public/                 # React build files
├── src/                    # React source code
├── venv/                   # Python virtual environment
├── tts_output/             # Generated audio files
├── episodes_data/          # Episode data files
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── package.json           # Node.js dependencies
```

## 🔍 Testing the Deployment

### Check Backend API
```bash
curl http://localhost:8000/api/episodes
```

### Check Frontend
```bash
curl http://localhost/
```

### Check Service Logs
```bash
# Backend logs
sudo journalctl -u allcanlearn -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🔄 Updating the Application

### Update Backend
```bash
cd /var/www/allcanlearn
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart allcanlearn
```

### Update Frontend
```bash
cd /var/www/allcanlearn
npm install
npm run build
cp -r build/* public/
```

## 📊 Monitoring

### Check System Resources
```bash
# Memory usage
free -h

# Disk usage
df -h

# Process status
ps aux | grep uvicorn
```

### Check Application Status
```bash
# Service status
sudo systemctl status allcanlearn

# Port usage
sudo netstat -tlnp | grep :8000
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Permission issues**
   ```bash
   sudo chown -R www-data:www-data /var/www/allcanlearn
   sudo chmod -R 755 /var/www/allcanlearn
   ```

3. **Python dependencies missing**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Nginx configuration error**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 🎯 Next Steps

1. **Domain Setup** - Point your domain to the server IP
2. **SSL Certificate** - Install SSL for HTTPS
3. **Monitoring** - Set up monitoring and alerts
4. **Backup** - Configure regular backups
5. **Scaling** - Consider load balancer for high traffic

## 📞 Support

If you encounter issues:
1. Check service logs: `sudo journalctl -u allcanlearn -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify all dependencies are installed
4. Ensure .env file has correct API keys

Your AllCanLearn v4 platform is now running on Ubuntu! 🎉
