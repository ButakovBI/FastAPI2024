import time
import aioredis
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.exc import SQLAlchemyError

from config import REDIS_HOST_TEST, REDIS_PORT_TEST


@pytest.mark.asyncio
async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post(
        "/operations",
        json={
            "id": 1,
            "quantity": "25.5",
            "figi": "figi_CODE",
            "instrument_type": "bond",
            "date": "2023-02-01T00:00:00",
            "type": "Выплата купонов",
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations",
                            params={"operation_type": "Выплата купонов"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1
    assert response.json()["details"] is None


@pytest.mark.asyncio
async def test_add_specific_operations_valid(ac: AsyncClient):
    response = await ac.post(
        "/operations",
        json={
            "id": 2,
            "quantity": "50.5",
            "figi": "figi_CODE_2",
            "instrument_type": "stock",
            "date": "2023-02-02T00:00:00",
            "type": "Дивиденды",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_get_specific_operations_with_different_type(ac: AsyncClient):
    response = await ac.get("/operations",
                            params={"operation_type": "Дивиденды"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1


@pytest.mark.asyncio
async def test_get_specific_operations_non_existent_type(ac: AsyncClient):
    response = await ac.get("/operations",
                            params={"operation_type": "NonExistentType"})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "data": response.json()["data"],
        "details": None}
    assert response.json()["status"] == "success"
    assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_add_specific_operations_invalid(ac: AsyncClient):
    response = await ac.post(
        "/operations",
        json={
            "id": 3,
            "quantity": 15,
            "figi": "figi_CODE_3",
            "instrument_type": "bond",
            "date": "2023-02-03T00:00:00",
            "type": "Выплата купонов",
        },
    )
    assert response.status_code == 422


@pytest.fixture(scope="session")
async def redis_test_cache():
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST_TEST}:{REDIS_PORT_TEST}",
        encoding="utf8",
        decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


@pytest.mark.asyncio
async def test_get_long_op_first(redis_test_cache, ac: AsyncClient):
    start_time = time.time()
    response = await ac.get("/operations/long_op")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    assert elapsed_time > 2

    assert response.status_code == 200
    assert response.json() == {
        "message": "long time operation successfully cached by redis"}


@patch("main.startup_event")
@pytest.mark.asyncio
async def test_get_long_op_cached(ac: AsyncClient):
    start_time = time.time()
    await ac.get("/operations/long_op")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    assert elapsed_time < 0.2


@pytest.mark.asyncio
async def test_get_specific_operations_success(ac: AsyncClient):
    response = await ac.get("/operations",
                            params={"operation_type": "Покупка"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_get_specific_operations_exception(ac: AsyncClient):
    with patch("database.get_async_session") as mock_get_session:
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("DB Error")
        mock_get_session.return_value.__aenter__.return_value = mock_session

        response = await ac.get("/operations",
                                params={"operation_type": "Покупка"})

        assert response.status_code == 200
