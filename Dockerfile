FROM python:3.9 as builder

WORKDIR /app

RUN apt-get update && apt-get -y upgrade

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN prisma generate

CMD ["python", "main.py"]
