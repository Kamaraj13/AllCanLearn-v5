# AllCanLearn 24/7 Systemd Service Setup

## Overview
AllCanLearn is configured to run 24/7 on Ubuntu using systemd services with automatic restart on failure and boot.

## Service Files Location
- `/etc/systemd/system/allcanlearn.service` - Main FastAPI application
- `/etc/systemd/system/allcanlearn-tunnel.service` - Cloudflare tunnel

## Service Configuration

### AllCanLearn App Service
```ini
[Unit]
Description=AllCanLearn FastAPI Application
After=network.target

[Service]
Type=simple
User=vikki
WorkingDirectory=/home/vikki/AllCanLearn
Environment=PATH=/home/vikki/AllCanLearn/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/vikki/AllCanLearn/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=append:/media/vikki/Data/AllCanLearn_Storage/logs/allcanlearn.log
StandardError=append:/media/vikki/Data/AllCanLearn_Storage/logs/allcanlearn.log

[Install]
WantedBy=multi-user.target
```

### Cloudflare Tunnel Service
```ini
[Unit]
Description=AllCanLearn Cloudflare Tunnel
After=network.target allcanlearn.service

[Service]
Type=simple
User=vikki
WorkingDirectory=/home/vikki/AllCanLearn
ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:8000
Restart=always
RestartSec=10
StandardOutput=append:/media/vikki/Data/AllCanLearn_Storage/logs/cloudflare_tunnel.log
StandardError=append:/media/vikki/Data/AllCanLearn_Storage/logs/cloudflare_tunnel.log

[Install]
WantedBy=multi-user.target
```

## Storage Configuration
All logs and TTS output are stored on the Data drive using symbolic links:
- **System Drive** (`/home/vikki/AllCanLearn`): 101MB (code + venv)
- **Data Drive** (`/media/vikki/Data/AllCanLearn_Storage/`): Growing content
  - `tts_output/` - AI-generated podcast audio files
  - `episodes_data/` - Episode metadata
  - `logs/` - Application and tunnel logs

## Management Commands

### Service Control
```bash
# Start services
sudo systemctl start allcanlearn.service
sudo systemctl start allcanlearn-tunnel.service

# Stop services
sudo systemctl stop allcanlearn.service
sudo systemctl stop allcanlearn-tunnel.service

# Restart services
sudo systemctl restart allcanlearn.service
sudo systemctl restart allcanlearn-tunnel.service

# Check status
sudo systemctl status allcanlearn.service
sudo systemctl status allcanlearn-tunnel.service

# Enable auto-start on boot
sudo systemctl enable allcanlearn.service
sudo systemctl enable allcanlearn-tunnel.service

# Disable auto-start
sudo systemctl disable allcanlearn.service
sudo systemctl disable allcanlearn-tunnel.service
```

### View Logs
```bash
# Live logs from systemd
journalctl -u allcanlearn.service -f
journalctl -u allcanlearn-tunnel.service -f

# Log files on Data drive
tail -f /media/vikki/Data/AllCanLearn_Storage/logs/allcanlearn.log
tail -f /media/vikki/Data/AllCanLearn_Storage/logs/cloudflare_tunnel.log

# Get current Cloudflare URL
grep 'trycloudflare.com' /media/vikki/Data/AllCanLearn_Storage/logs/cloudflare_tunnel.log | tail -1
```

### Process Monitoring
```bash
# Check if processes are running
ps aux | grep -E '(uvicorn|cloudflared)' | grep -v grep

# Check service health
systemctl is-active allcanlearn.service
systemctl is-enabled allcanlearn.service

# View service details
systemctl show allcanlearn.service
```

## Features

### Auto-Restart on Failure
- Services automatically restart after 10 seconds if they crash
- Unlimited restart attempts
- Logs capture all restart events

### Boot Persistence
- Both services start automatically on system boot
- Enabled with `systemctl enable` command
- Services start after network is available

### Resource Management
- Logs append (don't overwrite) to Data drive
- TTS files write to Data drive via symbolic links
- System drive stays lightweight for OS operations

## Troubleshooting

### Service Won't Start
```bash
# Check for errors
sudo systemctl status allcanlearn.service
journalctl -u allcanlearn.service -n 50

# Verify Python environment
/home/vikki/AllCanLearn/venv/bin/python --version
/home/vikki/AllCanLearn/venv/bin/uvicorn --version

# Test manual start
cd /home/vikki/AllCanLearn
venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Cloudflare URL Not Generating
```bash
# Check tunnel logs
tail -100 /media/vikki/Data/AllCanLearn_Storage/logs/cloudflare_tunnel.log

# Verify cloudflared installed
which cloudflared
cloudflared --version

# Test manual tunnel
cloudflared tunnel --url http://localhost:8000
```

### Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill old processes
sudo pkill -f 'uvicorn app.main'

# Restart service
sudo systemctl restart allcanlearn.service
```

## Access Points

### Local Access
- **Ubuntu Server**: http://192.168.1.138:8000
- **Same Network**: http://192.168.1.138:8000

### Global Access
- **Cloudflare Tunnel**: Check logs for current URL
- URL changes on tunnel restart (after reboot/crash)
- Example: https://dominant-jim-sheets-portraits.trycloudflare.com

## Capacity Planning

### Current Setup (4-5 Users)
- **Chat Messages**: In-memory (100 messages max)
- **TTS Audio**: 2-5 MB per podcast
- **Logs**: ~50 MB per month
- **Expected Growth**: 50-100 MB per month with cleanup

### Data Drive Space
- **Total**: 342 GB
- **Available**: 15 GB (user will clear to 100 GB)
- **Expected Lifetime**: 2+ years at current usage

## Backup Strategy

### Critical Data
- `/home/vikki/AllCanLearn/app/` - Application code
- `/home/vikki/AllCanLearn/.env` - Environment variables
- `/media/vikki/Data/AllCanLearn_Storage/episodes_data/` - Episode metadata

### Backup Commands
```bash
# Backup code
tar -czf allcanlearn-code-$(date +%Y%m%d).tar.gz /home/vikki/AllCanLearn/app

# Backup episodes
tar -czf allcanlearn-episodes-$(date +%Y%m%d).tar.gz /media/vikki/Data/AllCanLearn_Storage/episodes_data

# Backup configuration
cp /home/vikki/AllCanLearn/.env /home/vikki/AllCanLearn-env-backup-$(date +%Y%m%d)
```

## Maintenance Schedule

### Daily
- Check service status: `systemctl status allcanlearn`
- Monitor disk space: `df -h /media/vikki/Data`

### Weekly
- Review logs for errors
- Check Cloudflare tunnel stability
- Verify TTS file creation working

### Monthly
- Rotate old logs (keep last 3 months)
- Clean old TTS files (optional)
- Update Python dependencies if needed

## Updates and Deployment

### Update Code from GitHub
```bash
cd /home/vikki/AllCanLearn
git pull origin main
sudo systemctl restart allcanlearn.service
```

### Update Python Dependencies
```bash
cd /home/vikki/AllCanLearn
source venv/bin/activate
pip install --upgrade -r app/requirements.txt
deactivate
sudo systemctl restart allcanlearn.service
```

### Modify Service Configuration
```bash
# Edit service file
sudo nano /etc/systemd/system/allcanlearn.service

# Reload systemd
sudo systemctl daemon-reload

# Restart service
sudo systemctl restart allcanlearn.service
```
