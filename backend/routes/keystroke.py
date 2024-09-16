import json
from fastapi import APIRouter, WebSocket

from services.keystroke import KeyStrokeHandler
from model.keystroke_session import KeyStrokeSession

keystroke_router = APIRouter()

@keystroke_router.websocket("/register_keystrokes")
async def endpoint(websocket: WebSocket):
    await websocket.accept()
    keystroke_handler = KeyStrokeHandler()
    while True:
        try :
            data = await websocket.receive_text()
            json_data = json.loads(data)
            session = KeyStrokeSession(**json_data)
            response = keystroke_handler.session_handler(session)
            await websocket.send_text(response.to_json())
        except Exception as e:
            print(e)
            await websocket.send_text(f"An error occurred: {e}")
            websocket.close()