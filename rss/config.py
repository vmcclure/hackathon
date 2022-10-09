import os

MQ_HOST = os.environ["MQ_HOST"] if "MQ_HOST" in os.environ else "localhost"
MQ_PORT = int(os.environ["MQ_PORT"]) if "MQ_PORT" in os.environ else 5672
MQ_USER = os.environ["MQ_USER"] if "MQ_USER" in os.environ else "guest"
MQ_PASSWORD = os.environ["MQ_PASSWORD"] if "MQ_PASSWORD" in os.environ else "guest"

MONGO_HOST = os.environ["MONGO_HOST"] if "MONGO_HOST" in os.environ else "localhost"
MONGO_PORT = int(os.environ["MONGO_PORT"]) if "MONGO_PORT" in os.environ else 27017
MONGO_USER = os.environ["MONGO_USER"] if "MONGO_USER" in os.environ else ""
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"] if "MONGO_PASSWORD" in os.environ else ""
MONGO_DB = os.environ["MONGO_DB"] if "MONGO_DB" in os.environ else "rss"

URLS = [
        'https://rssexport.rbc.ru/rbcnews/news/1000/full.rss',
        'https://lenta.ru/rss/news',
]