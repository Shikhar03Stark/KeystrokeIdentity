
from typing import Optional
from pydantic import BaseModel, UUID4


class KeyStrokeSession(BaseModel):
    session_id: UUID4
    phrase_id: UUID4
    payload: str
    user_id: Optional[int] = -1