import aioredis
from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

from auth.base_config import auth_backend, fastapi_users_backend, current_user
from auth.models import User
from auth.schemas import UserCreate, UserRead

from operations.router import router as router_operation


app = FastAPI(title="Trading App")


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


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
