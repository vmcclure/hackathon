#!/usr/bin/python
# -*- coding: utf8 -*-

import json

from config import MQ_PASSWORD,MQ_HOST,MQ_PORT,MQ_USER
import pika

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

    def push_uploaded_tag(self,body, key="parser"):
        self.channel.basic_publish(exchange='', routing_key=key,
                                   body=body,
                                   properties=pika.BasicProperties(delivery_mode=2, ))

# text_header = "Скандально известный рэпер Паша Техник снимет на матче «Крыльев Советов» ток-шоу о легких деньгах"
# text_body = """
# В субботу, 9 марта, на матч «Крыльев Советов» и «Енисея» приедет популярный видеоблогер и рэпер Паша Техник. Об этом представители волжского клуба написали в социальных сетях.
#
# Паша Техник — скандально известный артист. Прославился благодаря выступлению на поэтическом состязании Versus Battle. Ролик с его участием набрал более 2,3 миллиона просмотров. Сейчас эпатажный рэпер снимает блог на YouTube о профессиях, при устройстве на которые не требуется высшее образование.
# """
# r = RABBIT()
# r.push_uploaded_tag(json.dumps({
#     'text_header': text_header,
#     'text_body': text_body
# }), key="parser")