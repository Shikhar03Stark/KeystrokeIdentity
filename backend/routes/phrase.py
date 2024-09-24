from fastapi import APIRouter

from services.phrase import PhraseCollection

phrase_router = APIRouter()

@phrase_router.get("/phrases")
def get_phrases(limit: int = 5):
    items = PhraseCollection.get_phrases(limit)
    return {"phrases": items, "count": len(items)}