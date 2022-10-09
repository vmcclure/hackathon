import psycopg2
import requests

from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from urllib.parse import urlparse

from xpath import FORUMS_SETTINGS

sanitizer = Sanitizer()


def get_body(url):
    url = url.replace("www.", "")
    if urlparse(url).netloc in FORUMS_SETTINGS:
        d = FORUMS_SETTINGS[urlparse(url).netloc]
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")
        news_text = soup.find(**d["find"])
        if not news_text:
            print(f"empty html or need another xpath {url}")
            return ""
        if d["rem"]:
            for rem in d["rem"]:
                for elem in news_text.find_all(**rem):
                    elem.decompose()
        sanitizer = Sanitizer()
        return (sanitizer.sanitize(news_text.text))
    else:
        print(f"need parser for {url}")
        return ""


def serialize(news):
    MODELS_TABLE = []
    for one_news in news:
        body = get_body(one_news['link'])
        if body:
            MODELS_TABLE.append({
                "text_header": one_news["title"],
                "published": one_news["published"],
                "text_body": body,
            })

    return MODELS_TABLE


def work_with_rss(resp, url):
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="postgres",
                                  host="postgres",
                                  port="5432",
                                  database="news")

    cur = connection.cursor()
    new_news = []
    current_date = None
    feed = feedparser.parse(resp)
    url = urlparse(url).netloc
    if not feed.entries:
        print("no rss feed", url)
    for elem in feed.entries:
        cur.execute(f"SELECT last_update from public.portal_update where url='{url}';")
        records = cur.fetchone()
        last_news_in_base = records[0]
        date_published = datetime.strptime(" ".join(elem["published"].split(" ")[:-1]), "%a, %d %b %Y %H:%M:%S")
        if not last_news_in_base or date_published.timestamp() > last_news_in_base.timestamp():
            new_news.append(elem)
            if not current_date or current_date < date_published:
                current_date = date_published
    if current_date:
        cur.execute(f'''UPDATE public.portal_update SET last_update='{current_date}' WHERE url='{url}';''')
    connection.commit()
    connection.close()
    if new_news:
        return serialize(new_news)
