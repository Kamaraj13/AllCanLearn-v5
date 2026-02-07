# chat.py - WebSocket chat manager for AllCanLearn Radio Station

from typing import List, Dict
import asyncio
import json
from datetime import datetime

class ConnectionManager:
    """WebSocket connection manager for real-time chat"""
    
    def __init__(self):
        self.active_connections: List[Dict] = []
        self.chat_history: Dict[str, List[Dict]] = {}
        self.max_history = 100
    
    async def connect(self, websocket, room: str = "default"):
        """Connect a new WebSocket client"""
        connection_info = {
            "websocket": websocket,
            "room": room,
            "connected_at": datetime.now()
        }
        self.active_connections.append(connection_info)
        
        # Initialize room history if needed
        if room not in self.chat_history:
            self.chat_history[room] = []
        
        return connection_info
    
    def disconnect(self, websocket):
        """Disconnect a WebSocket client"""
        self.active_connections = [
            conn for conn in self.active_connections 
            if conn["websocket"] != websocket
        ]
    
    async def send_personal_message(self, message: str, websocket):
        """Send message to specific client"""
        try:
            await websocket.send_text(message)
        except:
            # Connection closed
            self.disconnect(websocket)
    
    async def broadcast(self, message: str, room: str = "default"):
        """Broadcast message to all clients in a room"""
        # Store in history
        if room not in self.chat_history:
            self.chat_history[room] = []
        
        chat_message = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "room": room
        }
        
        self.chat_history[room].append(chat_message)
        
        # Keep only last N messages
        if len(self.chat_history[room]) > self.max_history:
            self.chat_history[room] = self.chat_history[room][-self.max_history:]
        
        # Broadcast to all connections in room
        disconnected = []
        for conn in self.active_connections:
            if conn["room"] == room:
                try:
                    await conn["websocket"].send_text(message)
                except:
                    disconnected.append(conn["websocket"])
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    def get_history(self, room: str = "default") -> List[Dict]:
        """Get chat history for a room"""
        return self.chat_history.get(room, [])

# Global manager instance
manager = ConnectionManager()
