from datetime import datetime
from typing import TypedDict
from uuid import UUID


class BillingDetail(TypedDict): ...


class Business(TypedDict):
    id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location_id: UUID
    billing_details: list[BillingDetail]

    # User attributes
    user_id: UUID
    notification_ids: list[UUID]
    active_status: bool
    created_datetime: datetime
    updated_datetime: datetime
