FROM python:3.13-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# Копирование проекта
COPY . .

# Собираем статику Django
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000


CMD ["gunicorn", "config:application", "--bind", "0.0.0.0:8000"]
