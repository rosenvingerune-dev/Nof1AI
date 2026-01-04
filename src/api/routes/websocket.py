from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from src.api.websocket import get_connection_manager, ConnectionManager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    manager: ConnectionManager = Depends(get_connection_manager)
):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            # Logic to handle incoming messages if we need bi-directional comms later
            # For now, just receive text to keep the loop valid
            data = await websocket.receive_text()
            # We could implement "ping/pong" here if needed
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        # Handle other exceptions (connection closed, etc)
        manager.disconnect(websocket)
