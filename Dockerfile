# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

CMD ["bash", "-c", "./wait-for-it.sh $DB_HOST 5432 -- python todo-cli.py"]
