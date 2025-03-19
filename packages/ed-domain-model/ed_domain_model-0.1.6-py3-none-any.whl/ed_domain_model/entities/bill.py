from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Bill(TypedDict):
    id: UUID
    business_id: UUID
    amount: float
    paid: bool
    create_datetime: datetime
    update_datetime: datetime
