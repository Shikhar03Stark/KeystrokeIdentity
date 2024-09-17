from typing import Optional
from pydantic import BaseModel

from model.user import UserSchema

class UserDTO(BaseModel):
    id: Optional[int] = -1
    username: str
    password: Optional[str] = ""
    signup_status: Optional[str] = "KEYSTROKE_PENDING" # KEYSTROKE_PENDING, COMPLETE
    signup_phrases_completed: Optional[int] = 0
    signup_phrases_target: Optional[int] = 5
        
    def from_schema(user_schema: UserSchema):
        return UserDTO(
            id=user_schema.id,
            username=user_schema.username,
            signup_status=user_schema.signup_status,
            signup_phrases_completed=user_schema.signup_phrases_completed,
            signup_phrases_target=user_schema.signup_phrases_target
        )
    