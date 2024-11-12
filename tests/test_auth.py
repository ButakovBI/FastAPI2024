from fastapi_users import BaseUserManager, IntegerIDMixin
import pytest
from sqlalchemy import insert, select

from auth.models import User, role
from auth.manager import UserManager
from auth.schemas import UserRead
from conftest import async_session_maker, client


@pytest.mark.asyncio
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, "admin", None)], "Роль не добавилась"


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "string",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "role_id": 1,
        },
    )

    assert response.status_code == 201


@pytest.fixture
async def test_user():
    async with async_session_maker() as session:
        new_user = User(
            email="string1@gmail.com",
            hashed_password="string",
            is_active=True,
            is_superuser=False,
            is_verified=False,
            username="string",
            role_id=1
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        user_read = UserRead(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            role_id=new_user.role_id,
            is_active=new_user.is_active,
            is_superuser=new_user.is_superuser,
            is_verified=new_user.is_verified
        )

        return user_read


# @pytest.mark.asyncio
# async def test_login_user(create_user_fixture):
#     response = client.post(
#         "/auth/jwt/login",
#         data={
#             "username": str(create_user_fixture.username),
#             "password": str(create_user_fixture.password)},
#         headers={
#             "Content-Type": "application/x-www-form-urlencoded"})
#     assert response.status_code == 204


@pytest.mark.asyncio
async def test_password_reset(create_user_fixture):
    token_response = client.post(
        "/auth/forgot-password", json={"email": create_user_fixture.email},
    )

    assert token_response.status_code == 202

    response = client.post(
        "/auth/reset-password", json={"token": "", "password": "newpassword"}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_user_verification(create_user_fixture):
    response = client.post(
        "/auth/login",
        json={
            "username": create_user_fixture.username,
            "password": create_user_fixture.password})
    client.post(
        "/auth/request-verify-token", json={"email": create_user_fixture.email}
    )
    response = client.post("/auth/verify", json={"token": ""})
    assert response.status_code == 400

# ---------------------------


@pytest.fixture
def auth_handler():
    return UserManager(IntegerIDMixin, BaseUserManager[User, int])


@pytest.mark.asyncio
async def test_on_after_request_verify(auth_handler, test_user):
    token = "sample_token"
    response = await auth_handler.on_after_request_verify(
        user=test_user,
        token=token
    )
    expected_message = (
        f"Verification requested for user {test_user.id}. "
        f"Verification token: {token}"
    )
    assert response["message"] == expected_message


@pytest.mark.asyncio
async def test_on_after_verify(auth_handler, test_user):
    response = await auth_handler.on_after_verify(user=test_user)
    assert response["message"] == \
        f"User {test_user.id} has been verified"


@pytest.mark.asyncio
async def test_on_after_forgot_password(auth_handler, test_user):
    token = "sample_token"
    response = await auth_handler.on_after_forgot_password(
        user=test_user, token=token
    )
    assert response["message"] == \
        f"User {test_user.id} has forgot their password. Reset token: {token}"


@pytest.mark.asyncio
async def test_on_after_reset_password(auth_handler, test_user):
    response = await auth_handler.on_after_reset_password(user=test_user)
    assert response["message"] == \
        f"User {test_user.id} has reset their password."


@pytest.mark.asyncio
async def test_on_before_delete(auth_handler, test_user):
    response = await auth_handler.on_before_delete(user=test_user)
    assert response["message"] == \
        f"User {test_user.id} is going to be deleted"


@pytest.mark.asyncio
async def test_on_after_delete(auth_handler, test_user):
    response = await auth_handler.on_after_delete(user=test_user)
    assert response["message"] == \
        f"User {test_user.id} is successfully deleted"
