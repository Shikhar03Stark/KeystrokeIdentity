import os
from dotenv import load_dotenv

config = {
    'dev': {
        'port': 5432,
        "db_username": "postgres",
        "db_password": "admin",
        "db_host": "localhost",
    },
    'prod': {
        'port': 3888,
    },
}

def load_env():
    load_dotenv()
    
def get_env():
    load_dotenv()
    value = os.getenv('ENV')
    return value if len(value) > 0 else 'dev'