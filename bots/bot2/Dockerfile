FROM python:3.13-slim

RUN apt-get update && apt-get install -y redis-server

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD redis-server --daemonize yes && python bot.py