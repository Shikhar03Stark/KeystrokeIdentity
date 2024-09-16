from fastapi import APIRouter, Response
from services.dto.user_dto import UserDTO
import services.auth as auth_service

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: UserDTO, response: Response):
    
    return auth_service.register_user(user, response)
    