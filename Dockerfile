FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN npm install prisma --save-dev

RUN PRISMA_PY_DEBUG_GENERATOR=1 python3 -m prisma generate

CMD ["python", "main.py"]
