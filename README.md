
---

# Шаблон MVP FastAPI

**Структура проекта для лёгкой дальнейшей разработки**

## О чём проект

Минималистичный шаблон с удобной структурой проекта для использования при создании MVP.

## Используемые технологии

| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) | ![Postgres](https://img.shields.io/badge/Postgres-336791?logo=postgresql&logoColor=white) | ![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white) | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white) | ![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white) |
|---|---|---|---|---|


## Работа с сервисом

Перед тем как развернуть сервис, необходимо установить [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/) на вашу машину.

Затем выполните следующие шаги:

1. **Клонируйте репозиторий:**

   ```bash
   git clone -b main https://github.com/ButakovBI/FastAPI2024.git
   ```

2. **Перейдите в директорию проекта:**

   ```bash
   cd FastAPI2024
   ```

3. **Запустите сервис:**

   ```bash
   docker-compose up -d --build
   ```

Теперь вы можете открыть в браузере [localhost](http://localhost:8000) и увидеть работающий сервис.

## Swagger-документация

FastAPI автоматически генерирует интерактивную документацию по доступным эндпоинтам API. Чтобы ознакомиться с ней и протестировать API прямо в браузере, перейдите по адресу:

[localhost:8000/docs](http://localhost:8000/docs)

Документация поддерживает Swagger UI, что позволяет легко отправлять запросы к API и видеть их результаты прямо в интерфейсе.

---
