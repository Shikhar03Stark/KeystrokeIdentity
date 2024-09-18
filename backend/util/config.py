import os
from dotenv import load_dotenv

config = {
    'dev': {
        'app_port': 8000,
        'db_port': 5433,
        "db_username": "keystroke",
        "db_password": "password",
        "db_host": "localhost",
        "jwt_secret": "keystroke_identity_000",
    },
    'prod': {
        'app_port': 3888,
    },
}

def load_env():
    load_dotenv()
    
def get_env():
    load_dotenv()
    value = os.getenv('ENV')
    return value if len(value) > 0 else 'dev'