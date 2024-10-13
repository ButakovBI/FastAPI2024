from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_client import Counter, Histogram, generate_latest
from redis import asyncio as aioredis
from starlette.responses import PlainTextResponse

from auth.base_config import auth_backend, current_user, fastapi_users_backend
from auth.models import User
from auth.schemas import UserCreate, UserRead
from config import REDIS_HOST, REDIS_PORT
from operations.router import router as router_operation
from pages.router import router as router_pages
from tasks.router import router as router_tasks

app = FastAPI(title="Template App")


REQUEST_COUNT = Counter("request_count", "Total number of requests")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of requests in seconds")


# @app.get("/")
# async def read_root():
#     REQUEST_COUNT.inc()
#     with REQUEST_LATENCY.time():
#         return {"message": "Hello, World!"}


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest())


@app.get("/", response_class=HTMLResponse)
async def read_root():
    base_dir = Path(__file__).resolve().parent

    html_path = base_dir / "templates" / "root.html"
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        return HTMLResponse(
            content=html_path.read_text(encoding="utf-8"), status_code=200
        )


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
