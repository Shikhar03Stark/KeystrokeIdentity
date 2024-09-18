from typing import Optional
from pydantic import BaseModel

class KeyStrokeVerifySession(BaseModel):
    mode: str #INIT, STROKE, NEXT, END
    payload: Optional[str] = ""
    username: Optional[str] = ""