FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/logs

COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

COPY . /app/
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "bwire_global_tech.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
