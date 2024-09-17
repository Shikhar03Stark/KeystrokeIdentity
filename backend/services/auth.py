from fastapi import HTTPException, Response
from util.config import get_env, config
from model.user import UserSchema
from database.db import conn
from database.user_table import UserTable
from services.dto.user_dto import UserDTO
import jwt
import hashlib

def _create_jwt_token(user: UserSchema):
    env = get_env()
    return jwt.encode({"username": user.username, "id": user.id}, config[env]["jwt_secret"], algorithm="HS256")

def _hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(user: UserSchema, response: Response):
    user_table = UserTable(conn=conn())
    exists = user_table.find_by_username(user.username)
    if exists is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    user.password = _hash_password(user.password)
    id = user_table.insert_one(user)
    response.status_code = 201
    user.id = id
    token = _create_jwt_token(user)
    response.headers['Token'] = f"Bearer {token}"
    return UserDTO.from_schema(user)

def manual_login(user: UserSchema, response: Response):
    user_table = UserTable(conn=conn())
    exists = user_table.find_by_username(user.username)
    user.password = _hash_password(user.password)
    if exists is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    if exists.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid password")
    response.status_code = 200
    token = _create_jwt_token(exists)
    response.headers['Token'] = f"Bearer {token}"
    return UserDTO.from_schema(exists)