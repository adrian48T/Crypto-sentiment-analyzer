import sqlite3
conn = sqlite3.connect('news.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    title TEXT,
    source TEXT,
    published TIMESTAMP,
    content TEXT,
    sentiment_label TEXT,
    sentiment_score REAL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
print('DB ready')
