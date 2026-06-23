from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import uuid

app = FastAPI()

rooms = {}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()

    if room_id not in rooms:
        rooms[room_id] = []

    rooms[room_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for client in rooms[room_id]:
                if client != websocket:
                    await client.send_text(data)

    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)

        if len(rooms[room_id]) == 0:
            del rooms[room_id]

@app.get("/create_room")
def create_room():
    room_id = str(uuid.uuid4())[:6]
    rooms[room_id] = []
    return {"room_id": room_id}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)