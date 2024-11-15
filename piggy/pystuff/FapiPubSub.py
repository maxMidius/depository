from fastapi import FastAPI, WebSocket
from fastapi.responses import WebSocketResponse

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections = {}  # {topic: set(websocket)}

    async def connect(self, websocket: WebSocket, topic: str):
        await websocket.accept()
        if topic not in self.connections:
            self.connections[topic] = set()
        self.connections[topic].add(websocket)
        print(f"Connected to topic {topic}")

    async def disconnect(self, websocket: WebSocket, topic: str):
        self.connections[topic].remove(websocket)
        print(f"Disconnected from topic {topic}")

    async def broadcast(self, topic, message):
        for connection in self.connections.get(topic, []):
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await manager.connect(websocket, topic)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(topic, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, topic)
