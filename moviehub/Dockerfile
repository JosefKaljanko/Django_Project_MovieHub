FROM --platform=linux/amd64 python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# systemové balíčky (hlavně pro psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements_minimum.txt .
RUN pip install --no-cache-dir -r requirements_minimum.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]