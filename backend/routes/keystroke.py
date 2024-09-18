import json
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketState

from model.keystroke_verify import KeyStrokeVerifySession
from model.keystroke_response import KeyStrokeResponse
from services.keystroke import KeyStrokeHandler, VerifyKeyStrokeHandler
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
            print(json_data)
            session = KeyStrokeSession(**json_data)
            response = keystroke_handler.session_handler(session)
            await websocket.send_text(response.to_json())
        except Exception as e:
            print(e)
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.send_text(KeyStrokeResponse(status="ERROR", payload=str(e)).to_json())
            break
    if websocket.client_state != WebSocketState.DISCONNECTED:
        await websocket.close()
        
@keystroke_router.websocket("/verify_keystrokes")
async def verify_keystrokes(websocket: WebSocket):
    await websocket.accept()
    keystroke_handler = VerifyKeyStrokeHandler()
    while True:
        try :
            data = await websocket.receive_text()
            json_data = json.loads(data)
            print(json_data)
            verify_session = KeyStrokeVerifySession(**json_data)
            response = keystroke_handler.verify_handler(verify_session)
            await websocket.send_text(response.to_json())
        except Exception as e:
            print(e)
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.send_text(KeyStrokeResponse(status="ERROR", payload=str(e)).to_json())
            break
    
    if websocket.client_state != WebSocketState.DISCONNECTED:
        await websocket.close()