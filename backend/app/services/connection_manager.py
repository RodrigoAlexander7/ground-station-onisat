"""
WebSocket connection manager for handling multiple clients.
"""
import asyncio
import json
import logging
from typing import Dict, Set

from fastapi import WebSocket

from app.core.models import SystemReading

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time data streaming.
    """
    
    def __init__(self):
        self._active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept and register a new WebSocket connection.
        """
        await websocket.accept()
        async with self._lock:
            self._active_connections.add(websocket)
        logger.info(f"WebSocket connected. Active: {len(self._active_connections)}")
    
    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection.
        """
        async with self._lock:
            self._active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Active: {len(self._active_connections)}")
    
    async def broadcast(self, reading: SystemReading) -> None:
        """
        Broadcast a reading to all connected clients.
        """
        if not self._active_connections:
            return
        
        message = reading.model_dump_json()
        
        # Create a copy to avoid modification during iteration
        async with self._lock:
            connections = self._active_connections.copy()
        
        disconnected = set()
        
        for connection in connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        if disconnected:
            async with self._lock:
                self._active_connections -= disconnected
    
    async def send_personal(self, websocket: WebSocket, data: dict) -> None:
        """
        Send a message to a specific client.
        """
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.warning(f"Failed to send personal message: {e}")
    
    @property
    def active_count(self) -> int:
        """
        Get the number of active connections.
        """
        return len(self._active_connections)


# Global connection manager instance
connection_manager = ConnectionManager()
