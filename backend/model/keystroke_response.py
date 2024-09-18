

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
        
class KeyStrokeVerifyResponse(BaseModel):
    status: str = "OK" # OK, ERROR
    payload: Optional[str] = ""
    user_id: Optional[int] = -1
    verify_confidence: Optional[float] = 0.0
    phrase_done: Optional[int] = 0
    
    def to_json(self):
        return str({
            'status': self.status,
            'payload': self.payload,
            'user_id': self.user_id,
            'verify_confidence': self.verify_confidence,
            'phrase_done': self.phrase_done
        })