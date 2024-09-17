from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    signup_status: Optional[str] = "KEYSTROKE_PENDING" # KEYSTROKE_PENDING, COMPLETE
    signup_phrases_completed: Optional[int] = 0
    signup_phrases_target: Optional[int] = 5
    
    # def __init__(self, id: int, username: str, password: str):
    #     self.id = id
    #     self.username = username
    #     self.password = password
        
    def __str__(self):
        return f'User(id={self.id}, username={self.username})'
    
    def __repr__(self):
        return self.__str__()
    
    def __to_dict__(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }