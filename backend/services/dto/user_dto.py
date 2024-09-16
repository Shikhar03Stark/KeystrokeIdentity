from typing import Optional
from pydantic import BaseModel

from model.user import UserSchema

class UserDTO(BaseModel):
    id: Optional[int] = -1
    username: str
    password: str | None
        
    def from_schema(user_schema: UserSchema):
        return UserDTO(
            id=user_schema.id,
            username=user_schema.username,
            password=user_schema.password
        )
    