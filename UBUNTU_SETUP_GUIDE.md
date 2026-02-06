# AllCanLearn - Ubuntu Server Setup Guide

Quick start guide to deploy AllCanLearn on your Ubuntu Server at **192.168.1.138**

## Prerequisites Checklist

- ✅ Ubuntu Server 22.04 LTS (or similar)
- ✅ SSH access as `vikki`
- ✅ Groq API Key (from https://console.groq.com)
- ✅ AllCanLearn repository (on Mac, ready to transfer)

## Option 1: Quick Transfer & Auto-Setup (Recommended)

### From Your Mac:

```bash
# Step 1: Navigate to workspace
cd ~/Desktop/AI\ Roundtable/AI-Roundtable

# Step 2: Copy AllCanLearn to Ubuntu server
scp -r AllCanLearn vikki@192.168.1.138:~/AllCanLearn

# Step 3: SSH into server and run automated setup
ssh vikki@192.168.1.138
cd ~/AllCanLearn
chmod +x setup-vm.sh
./setup-vm.sh
```

### What setup-vm.sh does:
- Updates system packages
- Installs Python 3.11, pip, git
- Installs espeak-ng (for TTS on Linux)
- Creates Python virtual environment
- Installs all dependencies from requirements.txt
- Creates .env file template
- Creates tts_output directory

### After Automated Setup:

```bash
# Edit .env to add your Groq API key
nano .env

# Key line to update:
# GROQ_API_KEY=your_key_here_from_console.groq.com
```

## Option 2: Test Run (Direct Execution)

```bash
# From Ubuntu server
cd ~/AllCanLearn
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Then from your Mac:
```bash
curl http://192.168.1.138:8001/
# Should return: {"status":"ok"}
```

## Option 3: Production Setup (Persistent Service)

### A. Using Supervisor + Nginx

```bash
# Install Supervisor (if not installed)
sudo apt-get install -y supervisor nginx

# Create supervisor config
sudo nano /etc/supervisor/conf.d/allcanlearn.conf
```

Paste this configuration:
```ini
[program:allcanlearn]
directory=/home/vikki/AllCanLearn
command=/home/vikki/AllCanLearn/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
autostart=true
autorestart=true
startsecs=10
stopasecs=10
redirect_stderr=true
stdout_logfile=/var/log/allcanlearn.log
environment=PATH="/home/vikki/AllCanLearn/venv/bin",PYTHONUNBUFFERED=1
```

Then enable it:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start allcanlearn
sudo supervisorctl status
```

### B. Configure Nginx Proxy

```bash
sudo nano /etc/nginx/sites-available/allcanlearn
```

Paste:
```nginx
upstream allcanlearn {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name 192.168.1.138;
    
    location / {
        proxy_pass http://allcanlearn;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_request_buffering off;
    }

    location /static/ {
        alias /home/vikki/AllCanLearn/app/static/;
        expires 30d;
    }

    location /tts_output/ {
        alias /home/vikki/AllCanLearn/tts_output/;
        expires 7d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/allcanlearn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl start nginx
sudo systemctl enable nginx
```

### C. Open Firewall

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw enable
```

**Now access at:** `http://192.168.1.138`

## Option 4: Docker Deployment

```bash
# Install Docker
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Logout and login again, then:
cd ~/AllCanLearn
docker-compose up --build -d

# Check status
docker-compose logs -f

# Stop/restart
docker-compose restart
docker-compose down
```

## Verification Steps

### 1. Is the app running?

```bash
# Via Supervisor
sudo supervisorctl status allcanlearn

# Via Docker  
docker ps | grep allcanlearn

# Direct check
curl http://127.0.0.1:8001/
```

### 2. Check logs for errors

```bash
# Supervisor logs
sudo tail -f /var/log/allcanlearn.log

# Docker logs
docker-compose logs -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### 3. Test from Mac

```bash
# Check podcast page works
curl http://192.168.1.138/ui

# Generate a quiz
curl -X POST http://192.168.1.138/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"topic":"Python", "difficulty":"easy", "num_questions":3}'

# Check chat endpoint
curl http://192.168.1.138/api/chat/online
```

## Accessing AllCanLearn

From **Mac or any device on your LAN:**

- **Main Page:** http://192.168.1.138
- **Podcast:** http://192.168.1.138/ui
- **Quiz:** http://192.168.1.138/quiz
- **API Docs:** http://192.168.1.138/docs
- **Chat:** Real-time WebSocket (integrated in pages)

## Common Issues & Solutions

### 1. "Connection refused" from Mac

```bash
# Check if app is running on Ubuntu
sudo supervisorctl status allcanlearn

# Check if Nginx is proxying correctly
sudo nginx -t
sudo systemctl status nginx

# Verify port 8001 is listening
netstat -tlnp | grep 8001
```

### 2. "Module not found" errors

```bash
# Reinstall dependencies
cd ~/AllCanLearn
source venv/bin/activate
pip install -r app/requirements.txt --upgrade
```

### 3. "GROQ_API_KEY not set"

```bash
# Check .env file
cat .env | grep GROQ

# Restart the service
sudo supervisorctl restart allcanlearn

# Verify it's set in the environment
source ~/.bashrc
echo $GROQ_API_KEY
```

### 4. TTS (Text-to-Speech) not generating audio

```bash
# Check espeak-ng is installed
which espeak-ng

# Test it manually
espeak-ng "Hello world" -w test.wav

# If not installed:
sudo apt-get install espeak-ng ffmpeg
```

### 5. Disk full from tts_output

```bash
# Check size
du -sh ~/AllCanLearn/tts_output/

# Clean files older than 30 days
find ~/AllCanLearn/tts_output -type f -mtime +30 -delete

# Set up automatic cleanup (cron job)
crontab -e
# Add: 0 2 * * * find /home/vikki/AllCanLearn/tts_output -mtime +30 -delete
```

## Monitoring & Maintenance

### Check system resources

```bash
# CPU, Memory, Disk
htop
df -h
du -sh ~/AllCanLearn

# App uptime
sudo supervisorctl status allcanlearn
```

### Update code

```bash
cd ~/AllCanLearn
git pull origin main
source venv/bin/activate
pip install -r app/requirements.txt
sudo supervisorctl restart allcanlearn
```

### View logs

```bash
# Real-time logs
sudo tail -f /var/log/allcanlearn.log

# Last 100 lines
sudo tail -100 /var/log/allcanlearn.log

# Search for errors
grep ERROR /var/log/allcanlearn.log
```

## Next Steps

### Phase 2 - Database Integration
- Switch from SQLite to PostgreSQL
- Enable user authentication (JWT)
- Store user progress and achievements

### Phase 3 - Advanced Features
- Add payment integration (Stripe)
- Implement subscription tiers
- Multi-AI provider support (OpenAI, Claude, Gemini)

### Phase 4 - Production Hardening
- SSL/TLS certificates (Let's Encrypt)
- Rate limiting
- Structured logging and monitoring
- Automated backups

## Quick Reference Commands

```bash
# SSH in
ssh vikki@192.168.1.138

# Navigate to app
cd ~/AllCanLearn

# Start service
sudo supervisorctl start allcanlearn

# Stop service
sudo supervisorctl stop allcanlearn

# Restart service
sudo supervisorctl restart allcanlearn

# View real-time logs
sudo tail -f /var/log/allcanlearn.log

# Check if listening
netstat -tlnp | grep 8001

# Test from Mac
curl http://192.168.1.138/

# Activate venv (if needed)
source ~/AllCanLearn/venv/bin/activate
```

## Support

- **App Logs:** `/var/log/allcanlearn.log`
- **Nginx Logs:** `/var/log/nginx/`
- **Full Docs:** See `DEPLOYMENT.md` for more details
- **Code:** See `README.md` for features and API endpoints

---

**Status:** AllCanLearn is ready to deploy! 🚀

All deployment files have been copied from the proven ai-roundtable_0.03 infrastructure.
