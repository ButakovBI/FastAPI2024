from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationResponse(BaseModel):
    status: str
    data: Optional[List[dict]]
    details: Optional[str]
