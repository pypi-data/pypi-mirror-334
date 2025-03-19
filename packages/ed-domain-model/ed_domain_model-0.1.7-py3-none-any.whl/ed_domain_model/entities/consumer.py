from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Consumer(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location_id: UUID

    # User attributes
    user_id: UUID
    notification_ids: list[UUID]
    active_status: bool
    created_datetime: datetime
    updated_datetime: datetime
