import psycopg2 as pg
from util.config import get_env, config

def conn() -> pg.connect:
    env = get_env()
    db_username = config[env]['db_username']
    db_password = config[env]['db_password']
    db_host = config[env]['db_host']
    db_name = 'keystroke'
    try:
        with pg.connect(host=db_host, database=db_name, user=db_username, password=db_password) as conn:
            print(f"Connected to {db_name} database")
            return conn
    except Exception as e:
        print(e)
        raise e
        