import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

DATABASE = {
    'host': os.getenv('PGHOST', 'pg'),
    'port': os.getenv('PGPORT', '5432'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', 'postgres'),
    'dbname': os.getenv('PGDATABASE', 'timeline'),
}

QDRANT_HOST = os.getenv('QDRANT_HOST', 'vector-db')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

COLLECTION = 'cards'


def get_conn():
    return psycopg2.connect(**DATABASE)


@app.on_event('startup')
def startup():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS cards (
        id BIGSERIAL PRIMARY KEY,
        url_hash TEXT UNIQUE,
        title TEXT,
        excerpt TEXT,
        tags TEXT[],
        published DATE,
        image_url TEXT
    );"""
    )
    conn.commit()
    cur.close()
    conn.close()

    import seed
    seed.seed()


@app.get('/timeline')
def timeline():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, title, excerpt, image_url, published FROM cards ORDER BY published DESC LIMIT 20"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@app.get('/card/{card_id}')
def get_card(card_id: int):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM cards WHERE id=%s", (card_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail='Card not found')
    return row


@app.get('/relate/{card_id}')
def relate(card_id: int):
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    search_res = client.search(
        collection_name=COLLECTION,
        query_filter=Filter(must=[FieldCondition(key='db_id', match=MatchValue(value=card_id))]),
        limit=1,
    )
    if not search_res:
        return []
    vector = search_res[0].vector
    related = client.search(collection_name=COLLECTION, query_vector=vector, limit=4)
    ids = [int(p.payload.get('db_id')) for p in related if int(p.payload.get('db_id')) != card_id][:3]
    if not ids:
        return []
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, title, excerpt, image_url, published FROM cards WHERE id = ANY(%s)", (ids,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
