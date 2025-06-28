import os
import psycopg2
from datetime import date

DATABASE = {
    'host': os.getenv('PGHOST', 'pg'),
    'port': os.getenv('PGPORT', '5432'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', 'postgres'),
    'dbname': os.getenv('PGDATABASE', 'timeline'),
}

rows = [
    {
        'url_hash': 'card1',
        'title': 'Card One',
        'excerpt': 'This is the first mock card used for the prototype.',
        'tags': ['news'],
        'published': date(2024, 1, 1),
        'image_url': 'https://placehold.co/600x400',
    },
    {
        'url_hash': 'card2',
        'title': 'Card Two',
        'excerpt': 'This is the second mock card used for the prototype.',
        'tags': ['updates'],
        'published': date(2024, 1, 2),
        'image_url': 'https://placehold.co/600x400',
    },
    {
        'url_hash': 'card3',
        'title': 'Card Three',
        'excerpt': 'This is the third mock card used for the prototype.',
        'tags': ['events'],
        'published': date(2024, 1, 3),
        'image_url': 'https://placehold.co/600x400',
    },
]


def seed():
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM cards')
    count = cur.fetchone()[0]
    if count == 0:
        for r in rows:
            cur.execute(
                'INSERT INTO cards (url_hash, title, excerpt, tags, published, image_url) VALUES (%s,%s,%s,%s,%s,%s)',
                (r['url_hash'], r['title'], r['excerpt'], r['tags'], r['published'], r['image_url'])
            )
        conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    seed()
