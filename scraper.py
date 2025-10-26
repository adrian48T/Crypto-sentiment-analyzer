from newspaper import Article
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_article(url):
    a = Article(url)
    a.download()
    a.parse()
    return {
        'url': url,
        'title': a.title or '',
        'content': a.text or '',
        'published': a.publish_date or datetime.utcnow()
    }

def get_urls_from_rss(rss_url):
    try:
        r = requests.get(rss_url, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')
        urls = [it.find('link').text for it in items if it.find('link')]
        return urls
    except Exception as e:
        print('rss fetch error', e)
        return []
