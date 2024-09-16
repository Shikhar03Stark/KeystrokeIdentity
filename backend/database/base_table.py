from typing import List
import psycopg2 as pg
from abc import ABC, abstractmethod

class CRUDTable(ABC):
    def __init__(self, conn: pg.connect):
        self.conn = conn

    @abstractmethod
    def insert_one(self, schema)-> int:
        pass
    
    @abstractmethod
    def insert_many(self, schemas: List):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass
    
    @abstractmethod
    def update(self, id: int, schema):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    def query(self, sql: str, params: tuple):
        pass
        