from typing import List
from fastapi import WebSocket
from src.gui.services.event_bus import get_event_bus, EventTypes
import logging
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.event_bus = get_event_bus()
        self.logger = logging.getLogger(__name__)
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Subscribe to EventBus and broadcast to all WS clients"""
        # Subscribe to all relevant event types
        event_types = [
            EventTypes.STATE_UPDATE,
            EventTypes.TRADE_EXECUTED,
            EventTypes.POSITION_OPENED,
            EventTypes.POSITION_CLOSED,
            EventTypes.ERROR_OCCURRED,
            EventTypes.BOT_STARTED,
            EventTypes.BOT_STOPPED,
            EventTypes.MARKET_DATA_UPDATE,
            EventTypes.PROPOSAL_CREATED
        ]
        
        for event_type in event_types:
            self.event_bus.subscribe(event_type, self._make_broadcast_handler(event_type))

    def _make_broadcast_handler(self, event_type: str):
        """Create a handler for a specific event type that calls broadcast"""
        # We need a closure here to capture event_type
        async def handler(data):
            message = {
                "type": event_type,
                "data": data,
                "timestamp": None  # Could add timestamp if needed
            }
            await self.broadcast(message)
        return handler

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"WebSocket client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.logger.info(f"WebSocket client disconnected. Remaining: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        if not self.active_connections:
            return
            
        # Convert dict to JSON string once
        try:
            # Handle non-serializable objects if necessary (e.g. datetime)
            # For now assuming data is serializable or Pydantic models with .dict()
            if hasattr(message.get('data'), 'dict'):
                 message['data'] = message['data'].dict()
                 
            # Basic JSON dump
            # Use default=str to handle datetime objects
            json_str = json.dumps(message, default=str)
            
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json_str)
                except Exception as e:
                    self.logger.warning(f"Failed to send to client: {e}")
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn)
                
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")

# Global instance
manager = ConnectionManager()

def get_connection_manager():
    return manager
