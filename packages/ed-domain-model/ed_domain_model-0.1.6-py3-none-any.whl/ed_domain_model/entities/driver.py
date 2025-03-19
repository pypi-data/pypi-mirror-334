from datetime import datetime
from typing import NotRequired, TypedDict
from uuid import UUID


class Driver(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    location_id: UUID
    car_id: UUID
    delivery_job_ids: list[UUID]
    payment_ids: list[UUID]

    # User attributes
    user_id: UUID
    notification_ids: list[UUID]
    active_status: bool
    created_datetime: datetime
    updated_datetime: datetime
