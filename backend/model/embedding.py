from typing import List, Optional
from pydantic import BaseModel

class EmbeddingSchema(BaseModel):
    id: Optional[int] = -1
    embedding: List[float]
    user_id: Optional[int] = -1
    purpose: Optional[str] = "SIGNUP" # SIGNUP, VERIFY, REINFORCE
    