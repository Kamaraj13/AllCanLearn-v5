# chat.py - WebSocket connection manager for real-time chat

from fastapi import WebSocket
from typing import List, Dict
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.message_history: List[Dict] = []
        self.max_history = 100

    async def connect(self, websocket: WebSocket, username: str = "Anonymous"):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        self.active_connections[username] = websocket
        
        # Send welcome message
        welcome_msg = {
            "type": "system",
            "message": f"{username} joined the chat",
            "timestamp": datetime.now().isoformat(),
            "online_count": len(self.active_connections)
        }
        await self.broadcast(welcome_msg)
        
        # Send recent messages to new user
        recent_messages = self.message_history[-50:] if len(self.message_history) > 50 else self.message_history
        for msg in recent_messages:
            await self.send_personal_message(msg, websocket)

    def disconnect(self, websocket: WebSocket) -> str:
        """Remove WebSocket connection and return username"""
        username = None
        for user, ws in self.active_connections.items():
            if ws == websocket:
                username = user
                break
        
        if username and username in self.active_connections:
            del self.active_connections[username]
        
        return username

    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error sending personal message: {e}")

    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for username, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting to {username}: {e}")
                disconnected.append(username)
        
        # Remove disconnected clients
        for username in disconnected:
            if username in self.active_connections:
                del self.active_connections[username]

    def add_to_history(self, message: Dict):
        """Add message to history, maintaining max size"""
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history = self.message_history[-self.max_history:]

    def get_online_users(self) -> List[str]:
        """Get list of online users"""
        return list(self.active_connections.keys())

    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

# Global manager instance
manager = ConnectionManager()
