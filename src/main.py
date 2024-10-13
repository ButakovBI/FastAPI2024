from pathlib import Path
import time
from redis import asyncio as aioredis
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import REGISTRY
from starlette.responses import PlainTextResponse
import uvicorn

from src.auth.base_config import auth_backend, fastapi_users_backend, current_user
from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead

from config import REDIS_HOST, REDIS_PORT

from operations.router import router as router_operation
from pages.router import router as router_pages
from tasks.router import router as router_tasks


app = FastAPI(title="Template App")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     base_dir = Path(__file__).resolve().parent

#     html_path = base_dir / "templates" / "root.html"

#     return HTMLResponse(content=html_path.read_text(encoding="utf-8"), status_code=200)


app.include_router(
    fastapi_users_backend.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users_backend.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users_backend.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users_backend.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
# REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])

# @app.middleware("http")
# async def monitor_requests(request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time

#     REQUEST_COUNT.labels(request.method, request.url.path).inc()

#     REQUEST_LATENCY.labels(request.url.path).observe(process_time)

#     return response

# # Эндпоинт для метрик
# @app.get("/metrics")
# async def metrics():
#     return PlainTextResponse(generate_latest(REGISTRY))


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
