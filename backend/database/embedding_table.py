from psycopg2 import connect
from typing import List
from model.embedding import EmbeddingSchema
from database.base_table import CRUDTable

class EmbeddingTable(CRUDTable):
    
    conn = None
    def __init__(self, conn: connect):
        super().__init__(conn)
        self.conn = conn
        
    def insert_one(self, schema:EmbeddingSchema):
        sql = """INSERT INTO "embeddings" (embedding, user_id, purpose) VALUES (%s, %s, %s) RETURNING id"""
        embedding_id = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (schema.embedding, schema.user_id, schema.purpose))
                rows = cur.fetchone()
                if rows:
                    embedding_id = rows[0]
                    
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            raise e
        finally:
            return embedding_id
        
    def get_closest_by_l2_norm(self, schema: EmbeddingSchema, top_n: int = -1):
        sql = """SELECT e.id, e.user_id, e.purpose, e.embedding from embeddings e ORDER BY e.embedding <-> %s::vector """
        if top_n > 0:
            sql += f" LIMIT {top_n}"
        embeddings = []
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (schema.embedding,))
                rows = cur.fetchall()
                if rows:
                    embeddings = [EmbeddingSchema(id=row[0], user_id=row[1], purpose=row[2], embedding=row[3]) for row in rows]
        except Exception as e:
            print(e)
        finally:
            return embeddings