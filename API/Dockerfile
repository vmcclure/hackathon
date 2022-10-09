FROM python:3.8

WORKDIR /app/

WORKDIR /app/
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt && \
   rm -rf /var/cache/apk/*

COPY . /app
ENV PYTHONUNBUFFERED=1

CMD python3 /app/manage.py runserver 0.0.0.0:8000