

from typing import Optional
from pydantic import BaseModel


class KeyStrokeResponse(BaseModel):
    
    status: str = "OK" # OK, ERROR
    payload: Optional[str] = ""
    
    def to_json(self):
        return str({
            'status': self.status,
            'payload': self.payload
        })