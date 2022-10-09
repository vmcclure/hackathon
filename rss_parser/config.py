import os

MQ_HOST = os.environ["MQ_HOST"] if "MQ_HOST" in os.environ else "localhost"
MQ_PORT = int(os.environ["MQ_PORT"]) if "MQ_PORT" in os.environ else 5672
MQ_USER = os.environ["MQ_USER"] if "MQ_USER" in os.environ else "guest"
MQ_PASSWORD = os.environ["MQ_PASSWORD"] if "MQ_PASSWORD" in os.environ else "guest"
