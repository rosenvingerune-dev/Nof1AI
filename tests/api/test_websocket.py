import pytest
from fastapi.testclient import TestClient
from src.api.main import app

def test_websocket_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        # Send a ping (just text in our simple implementation)
        websocket.send_text("ping")
        data = websocket.receive_text()
        assert data == "pong"

# Note: Testing the actual broadcasting from EventBus via WebSocket in unit tests 
# is complex because it requires running the event loop and the WebSocket handler 
# concurrently. For verify_websocket_broadcast, we rely on the manual integration 
# test (scripts/test_ws.py) or an E2E test with a running server.
# 
# However, we can test that the ConnectionManager subscribes to events.

from src.api.websocket import manager, EventTypes

def test_connection_manager_subscriptions():
    # Verify manager is subscribed to key events
    subscriptions = manager.event_bus._subscribers
    assert len(subscriptions[EventTypes.STATE_UPDATE]) > 0
    assert len(subscriptions[EventTypes.TRADE_EXECUTED]) > 0
