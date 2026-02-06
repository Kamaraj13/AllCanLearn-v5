"""
Real-time chat system using WebSockets
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
from datetime import datetime
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Dict] = []
        self.message_history: List[Dict] = []
        self.max_history = 100  # Keep last 100 messages
    
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        connection = {
            "websocket": websocket,
            "username": username,
            "connected_at": datetime.now().isoformat()
        }
        self.active_connections.append(connection)
        
        # Send message history to new user
        if self.message_history:
            await websocket.send_json({
                "type": "history",
                "messages": self.message_history[-50:]  # Last 50 messages
            })
        
        # Notify others
        await self.broadcast({
            "type": "system",
            "message": f"{username} joined the chat",
            "timestamp": datetime.now().isoformat(),
            "online_count": len(self.active_connections)
        }, exclude=websocket)
    
    def disconnect(self, websocket: WebSocket):
        connection = next((c for c in self.active_connections if c["websocket"] == websocket), None)
        if connection:
            self.active_connections.remove(connection)
            return connection["username"]
        return None
    
    async def broadcast(self, message: dict, exclude: WebSocket = None):
        """Send message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            if exclude and connection["websocket"] == exclude:
                continue
            try:
                await connection["websocket"].send_json(message)
            except:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        await websocket.send_json(message)
    
    def add_to_history(self, message: dict):
        """Store message in history"""
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
    
    def get_online_users(self) -> List[str]:
        """Get list of online usernames"""
        return [conn["username"] for conn in self.active_connections]


# Global connection manager
manager = ConnectionManager()
