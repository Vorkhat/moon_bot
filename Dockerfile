FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get -y upgrade && apt-get install -y git

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN prisma db push

CMD ["python", "main.py"]
