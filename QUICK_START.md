# AllCanLearn - Quick Reference Card

## 🚀 Deploy to Ubuntu in 3 Commands

```bash
# 1. From Mac - Transfer AllCanLearn to Ubuntu
scp -r ~/Desktop/AI\ Roundtable/AI-Roundtable/AllCanLearn vikki@192.168.1.138:~/

# 2. SSH into Ubuntu
ssh vikki@192.168.1.138

# 3. On Ubuntu - Run automated setup
cd ~/AllCanLearn && chmod +x setup-vm.sh && ./setup-vm.sh
```

Then edit `.env` with your Groq API key and run!

---

## 🎯 Run Options on Ubuntu

### Quick Test (Simplest)
```bash
cd ~/AllCanLearn
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001
# Visit: http://192.168.1.138:8001
```

### Production (Recommended)
```bash
# Supervisor auto-starts/restarts app
sudo nano /etc/supervisor/conf.d/allcanlearn.conf
# [Copy config from UBUNTU_SETUP_GUIDE.md]
sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl start allcanlearn

# Nginx proxies at port 80
sudo nano /etc/nginx/sites-available/allcanlearn
# [Copy config from UBUNTU_SETUP_GUIDE.md]
sudo ln -s /etc/nginx/sites-available/allcanlearn /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Then access at: http://192.168.1.138
```

### Docker (Containerized)
```bash
docker-compose up --build -d
```

---

## 📊 Access Points

| URL | Purpose | Status |
|-----|---------|--------|
| http://192.168.1.138 | Home page | ✅ |
| http://192.168.1.138/ui | Podcast player | ✅ |
| http://192.168.1.138/quiz | Quiz games | ✅ |
| http://192.168.1.138/docs | API docs | ✅ |
| WebSocket `/ws/chat` | Real-time chat | ✅ |

---

## 🔧 Service Management

```bash
# Check status
sudo supervisorctl status allcanlearn

# Start/Stop/Restart
sudo supervisorctl start allcanlearn
sudo supervisorctl stop allcanlearn
sudo supervisorctl restart allcanlearn

# View logs
sudo tail -f /var/log/allcanlearn.log

# Search for errors
grep ERROR /var/log/allcanlearn.log
```

---

## 🐛 Troubleshooting

### App won't start
```bash
# Check error logs
sudo tail -f /var/log/allcanlearn.log

# Check Python environment
source ~/AllCanLearn/venv/bin/activate
python -c "import fastapi; print('OK')"
```

### Can't connect from Mac
```bash
# From Ubuntu, check if listening
netstat -tlnp | grep 8001

# From Mac, test connectivity
ping 192.168.1.138
curl http://192.168.1.138:8001/
```

### GROQ_API_KEY not working
```bash
# Check .env file
cat ~/AllCanLearn/.env | grep GROQ

# Restart service to reload env
sudo supervisorctl restart allcanlearn

# Verify in logs
grep "GROQ_API_KEY" /var/log/allcanlearn.log
```

### TTS audio not generating
```bash
# Test espeak-ng
which espeak-ng
espeak-ng "test" -w /tmp/test.wav

# Install if missing
sudo apt-get install espeak-ng ffmpeg
```

---

## 📁 Important Files

```
~/AllCanLearn/
├── .env                    # ⚠️ Add your GROQ_API_KEY here
├── setup-vm.sh            # Run this first
├── UBUNTU_SETUP_GUIDE.md  # Detailed instructions
├── DEPLOYMENT_STATUS.md   # Full status report
├── app/main.py            # FastAPI application
├── app/static/            # Frontend (HTML/JS/CSS)
└── tts_output/            # Generated audio files
```

---

## 📋 Checklist Before Going Live

- [ ] AllCanLearn transferred to Ubuntu
- [ ] setup-vm.sh completed successfully
- [ ] .env file has valid GROQ_API_KEY
- [ ] App starts without errors: `sudo supervisorctl start allcanlearn`
- [ ] Can access from Mac: `curl http://192.168.1.138:8001/`
- [ ] Chat works: Connect to `http://192.168.1.138/ui` in browser
- [ ] Quiz page loads: Visit `http://192.168.1.138/quiz`
- [ ] Firewall allows port 80: `sudo ufw allow 80/tcp`

---

## 🎓 Features Included

✅ **Podcasts** - AI-generated episodes on any topic  
✅ **Quizzes** - Adaptive quiz system with scoring  
✅ **Chat** - Real-time WebSocket messaging  
✅ **Theme Toggle** - Dark/bright mode  
✅ **Responsive UI** - Works on mobile/tablet/desktop  
✅ **TTS Audio** - Text-to-speech generation  
✅ **Leaderboard** - Quiz rankings and stats  

---

## 🚀 Future Phases

**Phase 2:** Database (PostgreSQL) + User Auth (JWT)  
**Phase 3:** Multiple AI providers + Payment integration  
**Phase 4:** SSL/Monitoring + Advanced analytics  

---

## 📞 Support

1. **Check logs:** `sudo tail -f /var/log/allcanlearn.log`
2. **Read guide:** `UBUNTU_SETUP_GUIDE.md`
3. **Full status:** `DEPLOYMENT_STATUS.md`

---

**Status: Ready to Deploy** ✅

Last Updated: Jan 30, 2025
