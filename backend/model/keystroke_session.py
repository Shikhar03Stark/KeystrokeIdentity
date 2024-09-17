
from typing import Optional
from pydantic import BaseModel, UUID4


class KeyStrokeSession(BaseModel):
    mode: str # INIT, STROKE, NEXT, END
    payload: Optional[str] = ""
    session_id: Optional[int] = -1
    phrase_idx: Optional[int] = -1
    user_id: Optional[int] = -1