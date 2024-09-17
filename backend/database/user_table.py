from psycopg2 import connect
from typing import List
from model.user import UserSchema
from database.base_table import CRUDTable

class UserTable(CRUDTable):
    
    conn = None
    def __init__(self, conn: connect):
        super().__init__(conn)
        self.conn = conn
        
    def find_by_username(self, username: str):
        sql = """SELECT * FROM "users" u WHERE u.username = %s"""
        user = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (username,))
                row = cur.fetchone()
                if row:
                    user = UserSchema(id=row[0], username=row[1], password=row[2])
        except Exception as e:
            print(e)
        finally:
            return user
    
    def insert_one(self, schema: UserSchema):
        sql = """INSERT INTO "users" (username, password) VALUES (%s, %s) RETURNING id"""
        user_id = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (schema.username, schema.password))
                rows = cur.fetchone()
                if rows:
                    user_id = rows[0]
                    
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            return user_id
        
        
    def insert_many(self, schemas: List[UserSchema]):
        sql = """INSERT INTO "users" (username, password) VALUES (%s) RETURNING id"""
        user_ids = []
        try:
            with self.conn.cursor() as cur:
                cur.executemany(sql, [(schema.username, schema.password) for schema in schemas])
                rows = cur.fetchall()
                if rows:
                    user_ids = [row[0] for row in rows]
                    
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            return user_ids
        
    
    def delete(self, id: int):
        sql = """DELETE FROM "users" u WHERE u.id = %s"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (id,))
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            
            
    def update(self, id: int, schema: UserSchema):
        
        sql = """UPDATE "users" SET username = %s, password = %s WHERE id = %s"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (schema.username, schema.password, id))
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            
            
    def get_by_id(self, id: int):
        sql = """SELECT * FROM "users" u WHERE u.id = %s"""
        user = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (id,))
                row = cur.fetchone()
                if row:
                    user = UserSchema(id=row[0], username=row[1], password=row[2])
        except Exception as e:
            print(e)
        finally:
            return user
        
    def query(self, sql: str, params: tuple):
        users = []
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
                if rows:
                    users = [UserSchema(id=row[0], username=row[1], password=row[2]) for row in rows]
        except Exception as e:
            print(e)
        finally:
            return users