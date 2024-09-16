import os
from fastapi import FastAPI
from routes.register import register_routes
from util.config import config, load_dotenv
import util.log as log
from database.db import conn

load_dotenv()
conn()
log.info(f'Starting app in {os.getenv("ENV")} environment')
app = FastAPI()
register_routes(app) 
