"""
WebSocket chat endpoints - append to main.py
"""

CHAT_ENDPOINTS = '''

# ============= CHAT WEBSOCKET =============

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, username: str = "Anonymous"):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, username)
    
    # Send current online users
    await manager.send_personal_message({
        "type": "online_users",
        "users": manager.get_online_users(),
        "count": len(manager.active_connections)
    }, websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Create message object
            message = {
                "type": "message",
                "username": username,
                "message": data,
                "timestamp": datetime.now().isoformat()
            }
            
            # Add to history
            manager.add_to_history(message)
            
            # Broadcast to all clients
            await manager.broadcast(message)
            
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            # Notify others
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
