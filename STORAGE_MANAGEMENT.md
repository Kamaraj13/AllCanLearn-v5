# AllCanLearn - Storage & Message Management Guide

## 🌍 Current Setup for 24/7 Global Operations

Your AllCanLearn is now configured for:
- ✅ **24/7 Operation** - Always running for global users
- ✅ **Multi-Region Access** - Via Cloudflare Tunnel (no auth needed)
- ✅ **Auto-Restart** - Recovers from crashes automatically
- ✅ **Real-time Chat** - WebSocket-based messaging
- ✅ **118 GB Storage** - Available on Ubuntu server (96 GB free)

---

## 📊 Current Storage Usage

```
Total Disk Space:  118 GB
Currently Used:    17 GB (15%)
Available:         96 GB (85%)

AllCanLearn Directory:
├── app/            22 MB  (code & static files)
├── venv/           59 MB  (Python packages)
├── tts_output/     4 KB   (audio files)
└── logs/           ~124 KB (app logs)
```

---

## 💬 Message Storage Architecture

### Current System (In-Memory)

**Location:** `app/chat.py` - `ConnectionManager.message_history`

```
Storage Type:    In-Memory List (RAM)
Max Messages:    100 messages
Retention:       Last 100 messages per session
Persistence:     Session-based (lost on restart)
Size:            ~10 KB per 100 messages
Limit:           ≤1 MB for 10,000 messages
```

**How it works:**
- Messages stored in Python list during app runtime
- New chat connections receive last 50 messages
- Oldest messages deleted when exceeding 100 messages
- Lost when app restarts or crashes

### For 4-5 Global Users:
- ~10-20 messages per hour
- ~240-480 messages per day
- ~7,200-14,400 messages per month
- **Memory impact:** Negligible (< 5 MB)

---

## 🚀 Upgrade Path: Persistent Storage

### Option 1: SQLite (Simple, No Setup Needed)

**Pros:**
- File-based database
- No external services
- Perfect for 4-5 users
- Auto-backup with Git

**Cons:**
- Limited concurrency
- Slower than in-memory

**Setup:**
```bash
# On Ubuntu server
cd /home/vikki/AllCanLearn
pip install sqlalchemy
```

Then update `app/chat.py` to persist messages to SQLite.

### Option 2: PostgreSQL (Production-Ready)

**Pros:**
- Handles high concurrency
- Enterprise-grade reliability
- Scalable to 1000s of users

**Cons:**
- Requires installation
- More complex setup

**Setup:**
```bash
# On Ubuntu server
sudo apt-get install postgresql postgresql-contrib
createdb allcanlearn
```

### Option 3: Firebase/Firestore (Cloud-Based)

**Pros:**
- Fully managed
- Automatic backups
- Global replication
- Free tier available

**Cons:**
- External dependency
- Internet required

---

## 📁 Storage Management Strategy (24/7 Operation)

### 1. TTS Audio Files (Podcasts)

**Location:** `/home/vikki/AllCanLearn/tts_output/`

**Growth Rate:**
- 1 podcast = ~2-5 MB (depending on duration)
- 5 users × 2 podcasts/day = 20-50 MB/day
- Monthly growth: ~600-1500 MB

**Management:**
```bash
# Check TTS folder size
ssh vikki@192.168.1.138 "du -sh /home/vikki/AllCanLearn/tts_output"

# Archive old audio files (older than 30 days)
find /home/vikki/AllCanLearn/tts_output -type f -mtime +30 -delete

# Set up automatic cleanup (crontab)
0 2 * * * find /home/vikki/AllCanLearn/tts_output -mtime +30 -delete
```

### 2. Application Logs

**Location:** `/home/vikki/AllCanLearn/allcanlearn.log`

**Growth Rate:**
- ~10-50 KB per hour (with 4-5 users)
- ~240 KB - 1.2 MB per day
- Monthly growth: ~7-36 MB

**Management:**
```bash
# Check log size
ssh vikki@192.168.1.138 "du -h /home/vikki/AllCanLearn/allcanlearn.log"

# Archive and rotate logs
ssh vikki@192.168.1.138 "
  cd /home/vikki/AllCanLearn
  cp allcanlearn.log allcanlearn.log.$(date +%Y%m%d)
  > allcanlearn.log  # Clear the file
  gzip allcanlearn.log.*.gz  # Compress old logs
"

# Auto-rotate logs in crontab
0 0 * * 0 (cd /home/vikki/AllCanLearn && cp allcanlearn.log allcanlearn.log.bak && > allcanlearn.log)
```

### 3. Git Repository (Code & Backups)

**Location:** `/home/vikki/AllCanLearn/.git/`

**Size:** ~5-10 MB (minimal)

**Management:**
```bash
# Push changes to GitHub regularly
cd /home/vikki/AllCanLearn
git add .
git commit -m "Auto-save: $(date)"
git push origin main
```

---

## ⚠️ Disk Space Thresholds

| Used Space | Status | Action |
|-----------|--------|--------|
| < 50% | ✅ Healthy | No action needed |
| 50-75% | ⚠️ Warning | Monitor growth |
| 75-85% | 🔴 Critical | Archive old files |
| > 85% | 🛑 Danger | Immediate cleanup required |

**Current Status:** 15% used ✅

---

## 🔄 24/7 Operation - Maintenance Checklist

### Daily (Automated)
```bash
# Check app is running
ps aux | grep uvicorn | grep -v grep

# Monitor disk space
df -h /

# Check for crashes in logs
tail -100 /home/vikki/AllCanLearn/allcanlearn.log | grep -i error
```

### Weekly (Manual)
```bash
# Push code to GitHub
cd /home/vikki/AllCanLearn
git add . && git commit -m "Weekly backup" && git push

# Check chat messages count
# (Will vary based on user activity)

# Verify Cloudflare tunnel is running
ps aux | grep cloudflared | grep -v grep
```

### Monthly (Planning)
```bash
# Archive old TTS files
find /home/vikki/AllCanLearn/tts_output -mtime +30 -delete

# Rotate logs
# Analyze storage usage trends
du -sh /home/vikki/AllCanLearn/*

# Update documentation
# Plan for database migration if needed
```

---

## 🔐 Backup Strategy

### Automatic (Git)
```bash
# Every change is tracked in GitHub
# https://github.com/Kamaraj13/AllCanLearn
```

### Manual Backup (Weekly)
```bash
# Create compressed backup
ssh vikki@192.168.1.138 "
  cd /home/vikki
  tar -czf AllCanLearn.backup.$(date +%Y%m%d).tar.gz AllCanLearn/
  du -h AllCanLearn.backup.*.tar.gz
"

# Download to Mac for safekeeping
scp vikki@192.168.1.138:/home/vikki/AllCanLearn.backup.*.tar.gz ~/Backups/
```

---

## 📈 Growth Projections (4-5 Users)

### Month 1
```
TTS Files:     50-150 MB
Logs:          7-36 MB
Chat Messages: 7,200-14,400 (in-memory, ~10 MB)
Total:         ~70-200 MB
```

### Month 3
```
TTS Files:     150-450 MB (with cleanup: kept to 200 MB)
Logs:          21-108 MB (with rotation: kept to 50 MB)
Chat Messages: 21,600-43,200 (in-memory only)
Total:         ~270 MB (with cleanup)
```

### Year 1
```
With active cleanup:
- TTS Files:   ~2-5 GB (kept to 500 MB with 30-day rotation)
- Logs:        ~100 MB (with rotation)
- Code:        ~100 MB
Total:         ~700 MB (with proper management)
```

---

## 🚨 Disaster Recovery

### If App Crashes
```bash
# Automatic restart via loop script
# App will be back up in < 1 minute

# Manual restart if needed
ssh vikki@192.168.1.138 "
  cd /home/vikki/AllCanLearn
  pkill -f uvicorn
  nohup venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > allcanlearn.log 2>&1 &
"
```

### If Disk Gets Full
```bash
# Emergency cleanup
ssh vikki@192.168.1.138 "
  # Remove old TTS files
  find /home/vikki/AllCanLearn/tts_output -type f -delete
  
  # Rotate logs
  > /home/vikki/AllCanLearn/allcanlearn.log
  
  # Check results
  df -h /
"
```

### If GitHub Goes Down
```bash
# Local backup always exists
# Data is in /home/vikki/AllCanLearn/
# Create manual backup
tar -czf AllCanLearn.backup.tar.gz /home/vikki/AllCanLearn/
```

---

## 📊 Real-Time Monitoring Commands

### App Status
```bash
# Is it running?
ssh vikki@192.168.1.138 "ps aux | grep uvicorn"

# Port listening?
ssh vikki@192.168.1.138 "sudo netstat -tlnp | grep 8000"

# Recent errors?
ssh vikki@192.168.1.138 "tail -50 /home/vikki/AllCanLearn/allcanlearn.log | grep -i error"
```

### Storage Status
```bash
# Disk space
ssh vikki@192.168.1.138 "df -h /"

# AllCanLearn folder
ssh vikki@192.168.1.138 "du -sh /home/vikki/AllCanLearn && du -sh /home/vikki/AllCanLearn/*"

# Log file size
ssh vikki@192.168.1.138 "ls -lh /home/vikki/AllCanLearn/*.log"

# TTS folder size
ssh vikki@192.168.1.138 "du -sh /home/vikki/AllCanLearn/tts_output"
```

### Cloudflare Tunnel
```bash
# Is tunnel running?
ssh vikki@192.168.1.138 "ps aux | grep cloudflared | grep -v grep"

# Recent tunnel logs
ssh vikki@192.168.1.138 "tail -20 /home/vikki/AllCanLearn/cloudflare_tunnel.log"

# Get current public URL
ssh vikki@192.168.1.138 "grep 'trycloudflare.com' /home/vikki/AllCanLearn/cloudflare_tunnel.log | tail -1"
```

---

## 🎯 Next Steps

### Phase 1: Current (4-5 Users, In-Memory)
- ✅ Running 24/7
- ✅ Messages stored in RAM (up to 100)
- ✅ Backups via GitHub
- ✅ Free Cloudflare Tunnel
- **No action needed - works great!**

### Phase 2: 10-20 Users (Persistent Storage)
- Implement SQLite message persistence
- Auto-backup to S3 or backup service
- Monitor storage more closely
- Set up automated alerts

### Phase 3: 50+ Users (Enterprise)
- Migrate to PostgreSQL
- Implement proper database backups
- Add caching layer (Redis)
- Load balancing across multiple servers

---

## Summary

**For your current 4-5 global users:**
- ✅ 24/7 operation is ready
- ✅ In-memory chat storage is sufficient (100+ messages)
- ✅ 96 GB disk space is more than enough
- ✅ Auto-restart ensures uptime
- ✅ GitHub is your backup system
- ✅ Cloudflare Tunnel gives free global access

**No immediate action needed!** Monitor growth and upgrade when hitting 20+ concurrent users.
