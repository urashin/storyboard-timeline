import asyncio
from datetime import date
import hashlib
import os
import psycopg2
from playwright.async_api import async_playwright
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

DATABASE = {
    'host': os.getenv('PGHOST', 'pg'),
    'port': os.getenv('PGPORT', '5432'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', 'postgres'),
    'dbname': os.getenv('PGDATABASE', 'timeline'),
}

QDRANT_HOST = os.getenv('QDRANT_HOST', 'vector-db')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))
COLLECTION = 'cards'

URLS = [
    'https://example.org/',
    'https://example.org/about',
    'https://example.org/contact',
]


async def fetch(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        title = await page.title()
        content = await page.text_content('body')
        await browser.close()
        text = (content or '')[:300]
        return title, text


async def main():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    client.recreate_collection(collection_name=COLLECTION, vector_size=384, distance='Cosine')

    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()

    for url in URLS:
        title, text = await fetch(url)
        vector = model.encode(text)
        url_hash = hashlib.sha1(url.encode()).hexdigest()
        cur.execute(
            'INSERT INTO cards (url_hash, title, excerpt, tags, published, image_url)\n'
            'VALUES (%s,%s,%s,%s,%s,%s)\n'
            'ON CONFLICT (url_hash) DO UPDATE SET title = EXCLUDED.title RETURNING id',
            (url_hash, title, text, ['web'], date.today(), 'https://placehold.co/600x400')
        )
        card_id = cur.fetchone()[0]
        client.upsert(collection_name=COLLECTION, points=[
            (card_id, vector.tolist(), {'db_id': card_id})
        ])
    conn.commit()
    cur.close()
    conn.close()

asyncio.run(main())
