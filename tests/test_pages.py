from fastapi import FastAPI
from fastapi.testclient import TestClient

from pages.router import router as router_pages


app = FastAPI()
app.include_router(router_pages)

client = TestClient(app)


def test_get_root_page():
    response = client.get("/pages/")

    assert response.status_code == 200

    assert "<title>FastAPI MVP Template</title>" in response.text
    assert "<h1>Шаблон MVP FastAPI</h1>" in response.text
    assert "<h2>Используемые технологии</h2>" in response.text
    fastapi_message = (
        "FastAPI автоматически генерирует интерактивную документацию"
        " по доступным эндпоинтам API."
    )
    assert fastapi_message in response.text
    docs_href = (
        '<a href="http://localhost:8000/docs">localhost:8000/docs</a>'
    )

    assert docs_href in response.text

    assert 'alt="FastAPI"' in response.text
    assert 'alt="Postgres"' in response.text
    assert 'alt="Redis"' in response.text
    assert 'alt="Docker"' in response.text
    assert 'alt="Prometheus"' in response.text
    assert 'alt="Celery"' in response.text
