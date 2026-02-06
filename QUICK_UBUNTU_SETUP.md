# 🚀 Quick Ubuntu Server Setup for AllCanLearn v4

## 📋 Prerequisites
- Ubuntu 20.04+ server 
- SSH access to server
- Your AllCanLearn code (from current project)

## 🎯 Step-by-Step Setup

### 1. Copy Your Project to Ubuntu Server

**Option A: Using SCP (from your Mac)**
```bash
# From your Mac terminal, copy the entire project
scp -r /Users/vikki/Desktop/AI\ Roundtable/AI-Roundtable/AllCanLearn-v4/ vikki@YOUR_SERVER_IP:/home/vikki/

# SSH into your server
ssh vikki@YOUR_SERVER_IP
```

**Option B: Using Git (if you have a repo)**
```bash
# SSH into server first
ssh vikki@YOUR_SERVER_IP

# Clone your repository
git clone <YOUR_REPO_URL> AllCanLearn-v4
cd AllCanLearn-v4
```

### 2. Run the Ubuntu Deployment Script

```bash
# Make the script executable
chmod +x ubuntu_deploy.sh

# Run the deployment (this will install everything)
./ubuntu_deploy.sh
```

### 3. Update Your API Keys

```bash
# Edit the .env file with your actual API keys
nano .env

# Add your GROQ_API_KEY and other credentials
GROQ_API_KEY=your_actual_groq_key_here
```

### 4. Restart Services

```bash
# Restart the application
sudo supervisorctl restart allcanlearn

# Restart Nginx
sudo systemctl restart nginx
```

## 🌐 Access Your Application

Your app will be available at:
- **HTTP**: `http://YOUR_SERVER_IP`
- **HTTPS**: `https://YOUR_SERVER_IP` (after SSL setup)

## 🔧 What the Script Does Automatically

✅ **System Updates** - Updates Ubuntu packages  
✅ **Python Setup** - Installs Python 3.11 and virtual environment  
✅ **Dependencies** - Installs all required packages  
✅ **Database** - Sets up PostgreSQL (if needed)  
✅ **Web Server** - Configures Nginx reverse proxy  
✅ **Process Manager** - Sets up Supervisor for auto-restart  
✅ **Firewall** - Configures security settings  
✅ **Directories** - Creates all necessary folders  

## 📁 Directory Structure After Setup

```
/home/vikki/AllCanLearn-v4/
├── app/                    # Python backend
├── public/                 # React frontend
├── src/                    # React source
├── venv/                   # Python virtual env
├── tts_output/             # Audio files
├── episodes_data/          # Episode data
├── logs/                   # Application logs
└── .env                    # Environment variables
```

## 🔄 Making Updates

### Update Backend Code
```bash
cd /home/vikki/AllCanLearn-v4
git pull  # or scp new files
source venv/bin/activate
pip install -r app/requirements.txt
sudo supervisorctl restart allcanlearn
```

### Update Frontend
```bash
cd /home/vikki/AllCanLearn-v4
npm install
npm run build
cp -r build/* public/
```

## 📊 Monitoring

### Check Application Status
```bash
# Check if app is running
sudo supervisorctl status

# View logs
tail -f logs/app.log

# Check Nginx status
sudo systemctl status nginx
```

### Check Server Resources
```bash
# Memory usage
free -h

# Disk usage
df -h

# Process status
ps aux | grep uvicorn
```

## 🚨 Common Issues

### Port Already in Use
```bash
sudo lsof -i :8001
sudo kill -9 <PID>
```

### Permission Issues
```bash
sudo chown -R vikki:vikki /home/vikki/AllCanLearn-v4
sudo chmod -R 755 /home/vikki/AllCanLearn-v4
```

### Service Not Starting
```bash
# Check supervisor logs
sudo supervisorctl status allcanlearn
sudo tail -f /home/vikki/AllCanLearn-v4/logs/app.log
```

## 🔒 SSL Setup (Optional but Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🎯 Essential Topics Feature

Your Essential Topics 40-minute podcasts are already included! Once deployed:

1. **Click Essential Topics** in sidebar
2. **Generate 40-minute expert discussions**
3. **Auto-refresh every 3 days**
4. **Premium educational content**

## 📞 Quick Commands

```bash
# SSH into server
ssh vikki@YOUR_SERVER_IP

# Navigate to app
cd /home/vikki/AllCanLearn-v4

# Check status
sudo supervisorctl status

# View logs
tail -f logs/app.log

# Restart app
sudo supervisorctl restart allcanlearn

# Edit config
nano .env
```

## 🎉 Done!

Your AllCanLearn v4 platform is now running on Ubuntu with:
- ✅ Essential Topics (40-minute podcasts)
- ✅ Custom topic generation  
- ✅ Premium glassmorphism UI
- ✅ 3-day auto-cleanup
- ✅ Production-ready deployment

Access it at `http://YOUR_SERVER_IP` and start creating educational podcasts! 🚀
