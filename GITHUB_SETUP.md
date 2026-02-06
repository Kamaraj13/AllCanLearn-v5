# Push AllCanLearn to GitHub & Deploy on Ubuntu

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `AllCanLearn`
3. Description: `AI-powered learning platform with podcasts, quizzes, and real-time chat`
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**

## Step 2: Push to GitHub (From Your Mac)

```bash
cd ~/Desktop/AI\ Roundtable/AI-Roundtable/AllCanLearn

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AllCanLearn.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/vikki/AllCanLearn.git
git push -u origin main
```

## Step 3: Deploy on Ubuntu Server (192.168.1.138)

### SSH into your Ubuntu server:

```bash
ssh vikki@192.168.1.138
```

### Clone the repository:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/AllCanLearn.git
cd AllCanLearn
```

### Run the automated setup:

```bash
chmod +x setup-vm.sh
./setup-vm.sh
```

This will:
- Install Python 3.11
- Install espeak-ng (Linux TTS)
- Create virtual environment
- Install all dependencies
- Create .env template

### Configure your API key:

```bash
nano .env
```

Add your Groq API key:
```
GROQ_API_KEY=your_actual_key_here
```

Save with: `Ctrl+X`, then `Y`, then `Enter`

### Start AllCanLearn:

**Option A - Quick Test:**
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Access at: `http://192.168.1.138:8001`

**Option B - Production (Recommended):**

Follow the Supervisor setup in `UBUNTU_SETUP_GUIDE.md` for auto-restart on reboot.

## Step 4: Update Code (Future Changes)

### On Mac (after making changes):

```bash
cd ~/Desktop/AI\ Roundtable/AI-Roundtable/AllCanLearn
git add .
git commit -m "Description of changes"
git push
```

### On Ubuntu (pull latest changes):

```bash
cd ~/AllCanLearn
git pull
source venv/bin/activate
pip install -r app/requirements.txt  # If requirements changed
sudo supervisorctl restart allcanlearn  # If using supervisor
```

## Step 5: Make Public Globally (Optional)

### On Ubuntu, install Cloudflare tunnel:

```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# Start tunnel
./cloudflared-linux-amd64 tunnel --url http://localhost:8001
```

This will give you a public URL like: `https://something-random.trycloudflare.com`

## Quick Reference

```bash
# Clone on Ubuntu
git clone https://github.com/YOUR_USERNAME/AllCanLearn.git

# Setup
cd AllCanLearn && chmod +x setup-vm.sh && ./setup-vm.sh

# Configure
nano .env  # Add GROQ_API_KEY

# Run
source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8001

# Update later
git pull && pip install -r app/requirements.txt
```

## Troubleshooting

### Git push asks for username/password repeatedly

Use SSH instead:
```bash
# Generate SSH key on Mac (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/AllCanLearn.git
```

### Permission denied on Ubuntu

```bash
# Check if git is installed
sudo apt-get install git

# Configure git
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

### Can't access from Mac after starting on Ubuntu

```bash
# Check if app is running
ps aux | grep uvicorn

# Check if port is open
sudo ufw allow 8001/tcp

# Check if listening on all interfaces
netstat -tlnp | grep 8001
# Should show 0.0.0.0:8001, not 127.0.0.1:8001
```

## Support

- **Full deployment guide:** `UBUNTU_SETUP_GUIDE.md`
- **Quick start:** `QUICK_START.md`
- **Status info:** `DEPLOYMENT_STATUS.md`

---

**Ready to deploy!** 🚀
