FROM python:3.9-slim

WORKDIR /app/
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt && \
   rm -rf /var/cache/apk/*

COPY . /app
ENV PYTHONUNBUFFERED=1

CMD python3 /app/app.py