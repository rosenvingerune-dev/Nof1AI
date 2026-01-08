import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        
        # Send a ping
        await websocket.send("ping")
        response = await websocket.recv()
        print(f"Received: {response}")
        
        print("Waiting for events (press Ctrl+C to stop)...")
        while True:
            msg = await websocket.recv()
            print(f"Event received: {msg}")

if __name__ == "__main__":
    try:
        asyncio.run(test_ws())
    except KeyboardInterrupt:
        print("\nTest stopped")
    except Exception as e:
        print(f"Error: {e}")
