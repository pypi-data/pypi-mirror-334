from datetime import datetime
from typing import TypedDict
from uuid import UUID


class WarehouseWorker(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str

    # User attributes
    user_id: UUID
    notification_ids: list[UUID]
    active_status: bool
    created_datetime: datetime
    updated_datetime: datetime
