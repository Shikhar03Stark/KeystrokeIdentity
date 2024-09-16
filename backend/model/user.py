from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    
    # def __init__(self, id: int, username: str, password: str):
    #     self.id = id
    #     self.username = username
    #     self.password = password
        
    def __str__():
        return f'User(id={self.id}, username={self.username})'
    
    def __repr__():
        return self.__str__()
    
    def __to_dict__(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }