from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from auth.models import User
from auth.utils import get_user_db
from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        return {"message": f"User {user.id} has registered."}

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        return {"message": f"User {user.id} logged in."}

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        return {
            "message": f"Verification requested for user {user.id}. Verification token: {token}"
        }

    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        return {"message": f"User {user.id} has been verified"}

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        return {
            "message": f"User {user.id} has forgot their password. Reset token: {token}"
        }

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ):
        return {"message": f"User {user.id} has reset their password."}

    async def on_before_delete(self, user: User, request: Optional[Request] = None):
        return {"message": f"User {user.id} is going to be deleted"}

    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        return {"message": f"User {user.id} is successfully deleted"}


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
