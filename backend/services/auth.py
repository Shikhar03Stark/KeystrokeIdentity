from fastapi import HTTPException, Response
from model.user import UserSchema
from database.db import conn
from database.user_table import UserTable
from services.dto.user_dto import UserDTO

def register_user(user: UserSchema, response: Response):
    user_table = UserTable(conn=conn())
    exists = user_table.find_by_username(user.username)
    if exists is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    #Hash password
    id = user_table.insert_one(user)
    response.status_code = 201
    return UserDTO(id=id, username=user.username, password=user.password)