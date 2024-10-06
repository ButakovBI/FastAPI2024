from fastapi import Depends, FastAPI
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
