from typing import List
import psycopg2 as pg
from abc import ABC

class CRUDTable(ABC):
    def __init__(self, conn: pg.connect):
        self.conn = conn
        