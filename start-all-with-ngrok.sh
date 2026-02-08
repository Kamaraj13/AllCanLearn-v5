#!/bin/bash

# start-all-with-ngrok.sh - Start server + ngrok and print public URL

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting AI Roundtable + ngrok"

# Activate venv if available (for consistent python/pip/curl behavior)
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Start server in background if not already running
# DISABLED: Using direct server startup instead
# if ! pgrep -f "uvicorn ControlRoom.main:app" >/dev/null; then
#     echo "🎙️  Starting server in background..."
#     nohup "$SCRIPT_DIR/start-all.sh" > server.log 2>&1 &
#     sleep 3
# else
#     echo "✅ Server already running"
# fi

# Start ngrok in background if not already running  
# DISABLED: Ngrok disabled for now
# if ! pgrep -x "ngrok" >/dev/null; then
#     echo "🌐 Starting ngrok in background..."
#     nohup "$SCRIPT_DIR/start-ngrok-tunnel.sh" > ngrok.log 2>&1 &
#     sleep 3
# else
#     echo "✅ ngrok already running"
# fi

# Wait for ngrok API to be available and print public URL
# DISABLED: No ngrok URL needed
# echo "🔎 Fetching ngrok URL..."
# for i in {1..20}; do
#     if curl -s http://127.0.0.1:4040/api/tunnels >/dev/null 2>&1; then
#         break
    fi
    sleep 1
done

# DISABLED: No ngrok URL fetching
# PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 - <<'PY'
# import json,sys
# try:
#     data=json.load(sys.stdin)
#     for t in data.get("tunnels", []):
#         if t.get("public_url"):
#             print(t.get("public_url"))
#             break
# except Exception:
#     pass
# PY
# )

# if [ -n "$PUBLIC_URL" ]; then
#     echo "✅ Public URL: $PUBLIC_URL"
#     echo "🌍 Open: $PUBLIC_URL/ui"
# else
#     echo "⚠️  ngrok URL missing. Restarting ngrok..."
#     pkill -x "ngrok" >/dev/null 2>&1 || true
#     nohup "$SCRIPT_DIR/start-ngrok-tunnel.sh" > ngrok.log 2>&1 &
#     sleep 3

#     # Retry until public_url appears
#     for i in {1..20}; do
#         PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 - <<'PY'
# import json,sys
# try:
#     data=json.load(sys.stdin)
#     for t in data.get("tunnels", []):
#         if t.get("public_url"):
            #             print(t.get("public_url"))
#             break
#         except Exception:
#             pass
# PY
# )
#         if [ -n "$PUBLIC_URL" ]; then
#             break
#         fi
#         sleep 1
#     done

#     if [ -n "$PUBLIC_URL" ]; then
#         # echo "✅ Public URL: $PUBLIC_URL"
#         # echo "🌍 Open: $PUBLIC_URL/ui"
#     else
        echo "⚠️  Still no URL. Check logs:"
        echo "   - tail -f ngrok.log"
        echo "   - curl -s http://127.0.0.1:4040/api/tunnels"
    fi
fi