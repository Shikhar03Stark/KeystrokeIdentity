import os
from fastapi import FastAPI
from services.phrase import PhraseCollection
from routes.register import register_routes
from util.config import config, load_dotenv
import util.log as log
from fastapi.middleware.cors import CORSMiddleware
from database.db import conn
from typeformer.load import Transformer

load_dotenv()
conn()
log.info(f'Starting app in {os.getenv("ENV")} environment')
Transformer.get()
PhraseCollection.filepath = os.getenv("PHRASE_FILE") if os.getenv("PHRASE_FILE") is not None else "phrases.txt"
PhraseCollection.load_file()
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development purposes)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

register_routes(app) 
