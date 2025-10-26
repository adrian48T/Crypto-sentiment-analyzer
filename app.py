from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
from scraper import get_urls_from_rss, fetch_article
from sentiment import score_text
from datetime import datetime

app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
DB = 'news.db'

def save_article(a, label, score):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''INSERT OR IGNORE INTO articles (url,title,source,published,content,sentiment_label,sentiment_score)
                   VALUES (?,?,?,?,?,?,?)''', (
        a['url'], a['title'], 'rss', a.get('published'), a['content'], label, score
    ))
    conn.commit()
    conn.close()

def job_scrape():
    rss_list = [
        'https://cryptonews.com/news/rss/',
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'https://news.bitcoin.com/feed/'
    ]
    for rss in rss_list:
        urls = get_urls_from_rss(rss)
        for u in urls[:8]:
            try:
                art = fetch_article(u)
                if not art['content']:
                    continue
                label, score = score_text(art['content'])
                save_article(art, label, score)
            except Exception as e:
                print('article fetch error', e)

@app.route('/api/articles')
def list_articles():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    q = cur.execute('SELECT id,url,title,published,sentiment_label,sentiment_score FROM articles ORDER BY published DESC LIMIT 200')
    rows = [dict(id=r[0], url=r[1], title=r[2], published=r[3], sentiment_label=r[4], sentiment_score=r[5]) for r in q.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_scrape, 'interval', minutes=60)
    scheduler.start()
    print('Scheduler started')
    app.run(host='0.0.0.0', port=5000)
