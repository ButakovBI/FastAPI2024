import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(prefix="/operations", tags=["Operation"])


@router.get("")
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        data = [dict(row._mapping) for row in result.fetchall()]
        return {"status": "success", "data": data, "details": None}
    except Exception:
        raise HTTPException(
            status_code=500, detail={"status": "error", "data": None, "details": None}
        )


@router.post("")
async def add_specific_operations(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/long_op")
@cache(expire=30)
async def get_long_op():
    await asyncio.sleep(2)
    return {"message": "long time operation successfully cached by redis"}
