#!/bin/bash
# AllCanLearn 24/7 Startup Script with Auto-Restart
# Add this to crontab for persistent operation

cd /home/vikki/AllCanLearn

# Kill any existing processes
pkill -f "uvicorn app.main" 2>/dev/null

# Wait for cleanup
sleep 2

# Start Cloudflare tunnel (if not running)
if ! pgrep -f "cloudflared tunnel" > /dev/null; then
    nohup cloudflared tunnel --url http://localhost:8000 > cloudflare_tunnel.log 2>&1 &
    sleep 3
fi

# Start AllCanLearn with auto-restart on failure
while true; do
    source venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000 >> allcanlearn.log 2>&1
    
    # If it exits, wait 5 seconds and restart
    echo "$(date): AllCanLearn crashed, restarting in 5 seconds..." >> allcanlearn.log
    sleep 5
done &

# Log PID
echo $! > allcanlearn.pid
echo "AllCanLearn started with PID $(cat allcanlearn.pid)"
