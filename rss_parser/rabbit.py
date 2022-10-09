import json
from datetime import datetime

from config import MQ_PASSWORD, MQ_HOST, MQ_PORT, MQ_USER
import psycopg2
import pika

from ml_module import check_news
from news_compare import emotional_classification, ner_tagger, news_tagger


class RABBIT():
    def __init__(self):
        '''Подключение к rabbit'''
        print('connecting...')
        self.params = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT,
                                                credentials=pika.credentials.PlainCredentials(MQ_USER, MQ_PASSWORD))
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='parser', durable=True)

        print('connected')

    @staticmethod
    def listener():
        RABBIT().run()

    def callback(self, ch, method, properties, body):
        try:
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="postgres",
                                          host="postgres",
                                          port="5432",
                                          database="news")
            message = json.loads(body)
            new_text_header = message['text_header']
            print(new_text_header)
            new_text_body = message['text_body']
            date_news = datetime.strptime(" ".join(message["published"].split(" ")[:-1]), "%a, %d %b %Y %H:%M:%S")
            cur = connection.cursor()
            cur.execute("SELECT header, body from public.news;")
            records = cur.fetchall()
            cur.execute(f'''INSERT INTO public.all_news (body, news_date)
                             VALUES ('{new_text_body}', '{date_news}');''')

            if check_news(new_text_header, new_text_body, records):
                emo_color = emotional_classification(new_text_body)
                tag, tag_score = news_tagger(new_text_body)
                cur.execute(f'''INSERT INTO public.news (body, header, emo_color, news_date, tag, weight_tag)
                 VALUES ('{new_text_body}', '{new_text_header}', '{emo_color}', '{date_news}', '{tag}', '{tag_score}') RETURNING id;''')
                news_id = cur.fetchone()[0]
                for object_news, type_news in ner_tagger(new_text_body):
                    cur.execute(f'''INSERT INTO public.news_tag (news, object, type)
                                     VALUES ({news_id}, '{object_news}', '{type_news}');''')
            connection.commit()
            connection.close()
        except Exception as e:
            print(f'ERROR!!!{e}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('run')
        self.channel.basic_consume('parser', on_message_callback=self.callback)
        resp = self.channel.start_consuming()
        print(resp)

    def push_uploaded_tag(self, body):
        self.channel.basic_publish(exchange='', routing_key='data',
                                   body=body,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
