

from pydantic import BaseModel


class KeyStrokeInfo(BaseModel):
    event_type: str
    key: int
    timestamp: float