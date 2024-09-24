from fastapi import FastAPI
from routes.health_check import health_router
from routes.auth import auth_router
from routes.keystroke import keystroke_router
from routes.phrase import phrase_router

def register_routes(app: FastAPI):
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(keystroke_router)
    app.include_router(phrase_router)