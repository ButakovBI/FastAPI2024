FROM python:3.12-slim

WORKDIR /fastapi_app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh && chown -R appuser:appuser /fastapi_app

USER appuser

CMD ["docker/start.sh"]
