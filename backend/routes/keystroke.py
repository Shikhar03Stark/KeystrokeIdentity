from fastapi import APIRouter, WebSocket

from model.keystroke_session import KeyStrokeSession

keystroke_router = APIRouter()

@keystroke_router.websocket("/register_keystrokes")
async def endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        session = KeyStrokeSession(**json_data)
        await websocket.send_text(f"Message text was: {session.payload}")