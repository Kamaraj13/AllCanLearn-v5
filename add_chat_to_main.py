#!/usr/bin/env python3
"""Add WebSocket chat to main.py"""

# Read current main.py
with open('app/main.py', 'r') as f:
    content = f.read()

# Add imports at the top (after existing imports)
if 'from fastapi import WebSocket' not in content:
    # Find the line with 'from app.quiz_generator'
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Add after BackgroundScheduler import
        if 'from apscheduler.schedulers.background import BackgroundScheduler' in line:
            if i+1 < len(lines) and 'WebSocket' not in lines[i+1]:
                new_lines.append('from fastapi import WebSocket, WebSocketDisconnect')
                new_lines.append('from datetime import datetime')
        
        # Add after quiz_generator import
        if 'from app.quiz_generator import' in line:
            if i+1 < len(lines) and 'from app.chat import' not in lines[i+1]:
                new_lines.append('from app.chat import manager')
    
    content = '\n'.join(new_lines)

# Add WebSocket endpoints at the end
websocket_code = '''

# ============= CHAT WEBSOCKET =============

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, username: str = "Anonymous"):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, username)
    
    await manager.send_personal_message({
        "type": "online_users",
        "users": manager.get_online_users(),
        "count": len(manager.active_connections)
    }, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "message",
                "username": username,
                "message": data,
                "timestamp": datetime.now().isoformat()
            }
            manager.add_to_history(message)
            await manager.broadcast(message)
            
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast({
                "type": "system",
                "message": f"{username} left the chat",
                "timestamp": datetime.now().isoformat(),
                "online_count": len(manager.active_connections)
            })


@app.get("/api/chat/online")
def get_online_users():
    """Get currently online users"""
    return {
        "users": manager.get_online_users(),
        "count": len(manager.active_connections)
    }
'''

if '@app.websocket("/ws/chat")' not in content:
    content += websocket_code

# Write back
with open('app/main.py', 'w') as f:
    f.write(content)

print('✅ WebSocket chat endpoints added to main.py!')
